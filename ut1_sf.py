#!/usr/bin/env python
'''Unit test script for the Selenium Framework module.'''

import re
import os
import unittest
import selenium_framework as sf


#######################################################################
# Config

BROWSER = 'js' # Valid options: ff, gc, js, ie
BROWSER_OPTIONS = {
    'headless': True,
    'size': (800, 600),
    'position': (0, 0)
}
BROWSER_PROFILE = None
SELENIUM_HUB = 'local'
SELENIUM_PORT = '4444'
TEST_PAGE = f'file://{os.path.dirname(os.path.abspath(__file__))}/_sampleWebpage/TEST_PAGE.html'

#######################################################################

def intro_plan(title):
    '''Print a PLAN introduction.'''
    print(f'\n\n{"-" * 80}\n{title}\n{"-" * 80}', end='')

def intro_test(title):
    '''Print a TEST introduction.'''
    print(f'\n\t{title} '.ljust(65, '_'), end='')

class TestPlan001UtilityFunctions(unittest.TestCase):
    '''Set of test cases related to utility functions.'''
    def setUp(self):
        self.driver = sf.Driver()

    def tearDown(self):
        pass

    def test_001_date_time_functions(self):
        '''Test utility functions.'''
        intro_plan('Starting test plan 001 - Utility functions')
        intro_test('Test case 001 - Date and time functions')
        driver = self.driver
        current_date = driver.get_date()
        date_match = re.search('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', current_date)
        self.assertTrue(date_match is not None)

        current_time = driver.get_time()
        time_match = re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}$', current_time)
        self.assertTrue(time_match is not None)

    def test_002_make_valid_name(self):
        '''Test the make_valid_name method.'''
        intro_test('Test case 002 - Make valid name function')
        driver = self.driver
        test_string = '    Now-is the (time)    '
        result_string = driver.make_valid_name(test_string)
        self.assertTrue(result_string == 'Now_is_the_time')


class TestPlan002BasicBrowser(unittest.TestCase):
    '''Test basic browser functions.'''
    def setUp(self):
        self.driver = sf.Driver()
        self.driver.open(
            browser_name=BROWSER,
            selenium_hub=SELENIUM_HUB,
            selenium_port=SELENIUM_PORT
            )
        # self.driver.set_window(BROWSER_OPTIONS['size'], BROWSER_OPTIONS['position'])
        self.driver.goto(TEST_PAGE)

    def tearDown(self):
        self.driver.close()

    def test_001_open_and_close_test_page(self):
        '''Test opening and closing a browser with the test page.'''
        intro_plan('Starting test plan 002 - Basic browser functions')
        intro_test('Test case 001 - Open and close test page functions')
        driver = self.driver
        self.assertTrue(driver.browser.title == 'Test Page')

    def test_002_find_elements(self):
        '''Test the .find method.'''
        intro_test('Test case 002 - Find element functions')
        driver = self.driver

        # Single Element By ID
        element_list = driver.find('id=text01')
        self.assertTrue(isinstance(element_list, driver.WebElement))

        # Hidden element
        element_list = driver.find('id=hidden1')
        self.assertTrue(isinstance(element_list, driver.WebElement))
        self.assertFalse(driver.is_element_clickable(element_list))

        # Multiple Elements By Tag Name
        element_list = driver.find('tag=input')
        self.assertTrue(
            isinstance(element_list, list) and
            len(element_list) > 1 and
            isinstance(element_list[0], driver.WebElement)
            )

        # Invalid ID
        element_list = driver.find('id=alskdjflkajsldkfjlaksdf')
        self.assertTrue(
            isinstance(element_list, list) and
            len(element_list) == 0
            )

    def test_003_is_element_clickable(self):
        '''Test the .is_element_clickable method.'''
        intro_test('Test case 003 - Is element clickable functions')
        driver = self.driver

        clickable_element = driver.find('id=text01')
        self.assertTrue(driver.is_element_clickable(clickable_element))

        hidden_element = driver.find('id=hidden1')
        self.assertFalse(driver.is_element_clickable(hidden_element))

        hidden_element = driver.wait_until_element_clickable('id=hidden3')
        self.assertTrue(driver.is_element_clickable(hidden_element))
        self.assertTrue(isinstance(hidden_element, driver.WebElement))

    def test_004_text_fields(self):
        '''Test the .find method on text fields.'''
        intro_test('Test case 004 - Text field functions')
        driver = self.driver
        field_element = driver.find('id=text01')

        # Check initial value
        field_value = driver.is_field_set(field_element)
        self.assertEqual(field_value, 'Double-click me')

        # Set text field
        driver.set_field(field_element, 'Test123')
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == 'Test123')

        # Append to text field
        driver.set_field(field_element, '456', append=True)
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == 'Test123456')

        # Change text field value
        driver.set_field(field_element, '456')
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == '456')

        # Clear text field
        driver.set_field(field_element, '')
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == '')

    def test_005_select_fields(self):
        '''Test the .find method on select fields.'''
        intro_test('Test case 005 - Select field functions')
        driver = self.driver
        field_element = driver.find('id=select02')

        # Is field not set
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == [])

        # Set select field
        driver.set_field(field_element, [1, 3, 4])
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == ['1', '3', '4'])

        # Add values to select field
        driver.set_field(field_element, [2, 5], append=True)
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == ['1', '2', '3', '4', '5'])

        # Change select field value
        driver.set_field(field_element, [2, 5])
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == ['2', '5'])

        # Clear select field
        driver.set_field(field_element, [])
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == [])

    def test_006_text_area(self):
        '''Test the .find method on text area fields.'''
        intro_test('Test case 006 - Text area functions')
        driver = self.driver
        field_element = driver.find('id=textarea01')

        # Check initial value
        field_value = driver.is_field_set(field_element)
        self.assertEqual(field_value, 'Right-click me')

        # Set text field
        driver.set_field(field_element, 'Test123')
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == 'Test123')

        # Append to text field
        driver.set_field(field_element, '456', append=True)
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == 'Test123456')

        # Change text field value
        driver.set_field(field_element, '456')
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == '456')

        # Clear text field
        driver.set_field(field_element, '')
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value == '')

    def test_007_checkbox(self):
        '''Test the .find method on checkbox fields.'''
        intro_test('Test case 007 - Checkbox functions')
        driver = self.driver
        field_locator = 'id=chbox01'
        field_element = driver.find(field_locator)

        # Checkbox is not set
        field_value = driver.is_field_set(field_element)
        self.assertFalse(field_value)

        # Set checkbox
        driver.set_field(field_element, True)
        field_value = driver.is_field_set(field_element)
        self.assertTrue(field_value)

        # Clear checkbox
        driver.set_field(field_element, False)
        field_value = driver.is_field_set(field_element)
        self.assertFalse(field_value)

    def test_008_radio_buttons(self):
        '''Test the .find method on radio button fields.'''
        intro_test('Test case 008 - Radio button functions')
        driver = self.driver
        field_locator = 'name=radio'
        field_element = driver.find(field_locator)

        # Radio is not set
        field_value = driver.is_radio_button_group_set(field_element)
        self.assertFalse(field_value)

        # Set radio button
        field_element[1].click()
        field_value = driver.is_radio_button_group_set(field_element)
        self.assertTrue(field_value == ['Value 1'])


class TestPlan003AdvancedFeatures(unittest.TestCase):
    '''Test the advanced features.'''
    def setUp(self):
        self.driver = sf.Driver()
        self.driver.open(
            browser_name=BROWSER,
            selenium_hub=SELENIUM_HUB,
            selenium_port=SELENIUM_PORT
            )
        # self.driver.set_window(BROWSER_OPTIONS['size'], BROWSER_OPTIONS['position'])
        self.driver.goto(TEST_PAGE)

    def tearDown(self):
        self.driver.close()

    def test_001_double_click_and_alert(self):
        '''Test the .double_click method.'''
        intro_plan('Starting test plan 003 - Advanced features functions')
        intro_test('Test case 001 - Double-click functions')
        # if config.BROWSER == 'js':
        #     raise Exception('Skipping popup test in a headless browser.')
        driver = self.driver
        field_locator = 'id=text01'
        field_element = driver.find(field_locator)
        self.assertTrue(driver.double_click(field_element))
        alert_text = driver.check_alert()
        self.assertTrue(alert_text == 'Double-click event')

    def test_002_right_click_and_alert(self):
        '''Test the .right_click method.'''
        intro_test('Test case 002 - Right-click functions')
        # if config.BROWSER == 'js':
        #     raise Exception('Skipping popup test in a headless browser.')
        driver = self.driver
        field_locator = 'id=textarea01'
        field_element = driver.find(field_locator)
        self.assertTrue(driver.right_click(field_element))
        alert_text = driver.check_alert()
        self.assertTrue(alert_text == 'Right-click event')


# ############################################################################
# def TEMPLATE_test_000_name(self):
#     d = self.driver
#     d.open()
#     d.goto(URL)
#     '''Do something here'''
#     d.close()
#
# def TEMPLATE_test_000_do_something(self):
#     d = self.driver
#     field_locator = 'id=select02'
#     field_element = d.find(field_locator)
#     # do something here
#     self.assertTrue(False)
#
#  ############################################################################


if __name__ == '__main__':
    unittest.main(warnings='ignore')
