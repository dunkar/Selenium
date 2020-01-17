#!/usr/bin/env python
# Unit test script for the Selenium Framework module.

import re
import unittest
import selenium_framework as sf
import config


class TestPlan001UtilityFunctions(unittest.TestCase):
    def setUp(self):
        self.driver = sf.Driver()

    def tearDown(self):
        pass

    def test_001_date_time_functions(self):
        print('\n\nStarting test plan 001 - Utility functions:', end='')
        print('\nStarting test case 001 - Date and time functions: ', end='')
        d = self.driver
        current_date = d.get_date()
        date_match = re.search('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', current_date)
        self.assertTrue(date_match is not None)

        current_time = d.get_time()
        time_match = re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}$', current_time)
        self.assertTrue(time_match is not None)

    def test_002_make_valid_name(self):
        print('\nStarting test case 002 - Make valid name function: ', end='')
        d = self.driver
        test_string = '    Now-is the (time)    '
        result_string = d.make_valid_name(test_string)
        self.assertTrue(result_string == 'Now_is_the_time')


class TestPlan002BasicBrowser(unittest.TestCase):
    def setUp(self):
        self.driver = sf.Driver()
        self.driver.open(
            browser_name=config.browser_name,
            selenium_hub=config.selenium_hub,
            selenium_port=config.selenium_port
            )
        self.driver.set_window(config.browser_size, config.browser_position)
        self.driver.goto(config.test_page)

    def tearDown(self):
        self.driver.close()

    def test_001_open_and_close_test_page(self):
        print('\n\nStarting test plan 002 - Basic browser functions.', end='')
        print('\nStarting test case 001 - Open and close test page functions: ', end='')
        d = self.driver
        self.assertTrue(d.browser.title == 'Test Page')

    def test_002_find_elements(self):
        print('\nStarting test case 002 - Find element functions: ', end='')
        d = self.driver

        # Single Element By ID
        element_list = d.find('id=text01')
        self.assertTrue(isinstance(element_list, d.WebElement))

        # Hidden element
        element_list = d.find('id=hidden1')
        self.assertTrue(isinstance(element_list, d.WebElement))
        self.assertFalse(d.is_element_clickable(element_list))

        # Multiple Elements By Tag Name
        element_list = d.find('tag=input')
        self.assertTrue(
            isinstance(element_list, list) and
            len(element_list) > 1 and
            isinstance(element_list[0], d.WebElement)
            )

        # Invalid ID
        element_list = d.find('id=alskdjflkajsldkfjlaksdf')
        self.assertTrue(
            isinstance(element_list, list) and
            len(element_list) == 0
            )

    def test_003_is_element_clickable(self):
        print('\nStarting test case 003 - Is element clickable functions: ', end='')
        d = self.driver

        clickable_element = d.find('id=text01')
        self.assertTrue(d.is_element_clickable(clickable_element))

        hidden_element = d.find('id=hidden1')
        self.assertFalse(d.is_element_clickable(hidden_element))

        hidden_element = d.wait_until_element_clickable('id=hidden3')
        self.assertTrue(d.is_element_clickable(hidden_element))
        self.assertTrue(isinstance(hidden_element, d.WebElement))

    def test_004_text_fields(self):
        print('\nStarting test case 004 - Text field functions: ', end='')
        d = self.driver
        field_element = d.find('id=text01')

        # Is field empty
        field_value = d.is_field_set(field_element)
        self.assertFalse(field_value)

        # Set text field
        d.set_field(field_element, 'Test123')
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == 'Test123')

        # Append to text field
        d.set_field(field_element, '456', append=True)
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == 'Test123456')

        # Change text field value
        d.set_field(field_element, '456')
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == '456')

        # Clear text field
        d.set_field(field_element, '')
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == '')

    def test_005_select_fields(self):
        print('\nStarting test case 005 - Select field functions: ', end='')
        d = self.driver
        field_element = d.find('id=select02')

        # Is field not set
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == [])

        # Set select field
        d.set_field(field_element, [1, 3, 4])
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == ['1', '3', '4'])

        # Add values to select field
        d.set_field(field_element, [2, 5], append=True)
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == ['1', '2', '3', '4', '5'])

        # Change select field value
        d.set_field(field_element, [2, 5])
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == ['2', '5'])

        # Clear select field
        d.set_field(field_element, [])
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == [])

    def test_006_text_area(self):
        print('\nStarting test case 006 - Text area functions: ', end='')
        d = self.driver
        field_element = d.find('id=textarea01')

        # Is field empty
        field_value = d.is_field_set(field_element)
        self.assertFalse(field_value)

        # Set text field
        d.set_field(field_element, 'Test123')
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == 'Test123')

        # Append to text field
        d.set_field(field_element, '456', append=True)
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == 'Test123456')

        # Change text field value
        d.set_field(field_element, '456')
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == '456')

        # Clear text field
        d.set_field(field_element, '')
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value == '')

    def test_007_checkbox(self):
        print('\nStarting test case 007 - Checkbox functions: ', end='')
        d = self.driver
        field_locator = 'id=chbox01'
        field_element = d.find(field_locator)

        # Checkbox is not set
        field_value = d.is_field_set(field_element)
        self.assertFalse(field_value)

        # Set checkbox
        d.set_field(field_element, True)
        field_value = d.is_field_set(field_element)
        self.assertTrue(field_value)

        # Clear checkbox
        d.set_field(field_element, False)
        field_value = d.is_field_set(field_element)
        self.assertFalse(field_value)

    def test_008_radio_buttons(self):
        print('\nStarting test case 008 - Radio button functions: ', end='')
        d = self.driver
        field_locator = 'name=radio'
        field_element = d.find(field_locator)

        # Radio is not set
        field_value = d.is_radio_button_group_set(field_element)
        self.assertFalse(field_value)

        # Set radio button
        field_element[1].click()
        field_value = d.is_radio_button_group_set(field_element)
        self.assertTrue(field_value == ['Value 1'])


class TestPlan003AdvancedFeatures(unittest.TestCase):
    def setUp(self):
        self.driver = sf.Driver()
        self.driver.open(
            browser_name=config.browser_name,
            selenium_hub=config.selenium_hub,
            selenium_port=config.selenium_port
            )
        self.driver.set_window(config.browser_size, config.browser_position)
        self.driver.goto(config.test_page)

    def tearDown(self):
        self.driver.close()

    def test_001_double_click_and_alert(self):
        print('\n\nStarting test plan 003 - Advanced features functions.', end='')
        print('\nStarting test case 001 - Double-click functions: ', end='')
        d = self.driver
        field_locator = 'id=text01'
        field_element = d.find(field_locator)
        self.assertTrue(d.double_click(field_element))
        alert_text = d.check_alert()
        self.assertTrue(alert_text == 'Double-click event')

    def test_002_right_click_and_alert(self):
        print('\nStarting test case 002 - Right-click functions: ', end='')
        d = self.driver
        field_locator = 'id=chbox01'
        field_element = d.find(field_locator)
        self.assertTrue(d.right_click(field_element))
        alert_text = d.check_alert()
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
