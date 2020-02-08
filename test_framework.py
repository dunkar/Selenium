#!/usr/bin/env python
'''
This script tests basic functionality of the Selenium Framework.
Execute this script by running "pytest -s" in the directory containing
the script and framework files.
'''

import os
import re
import selenium_framework as sf

CONFIG = {
    'browser': 'Chrome',
    'headless': True,
    'profile': '/Users/john/Library/Application Support/Google/Chrome/selenium',
    'browser_size': (800, 600),
    'browser_position': (0, 0),
    'remote_hub': False,    # (server_name_or_ip, port),
    'test_page': f'file://{os.path.dirname(os.path.abspath(__file__))}/test_page.html'
}

def intro_plan(title):
    '''Print a PLAN introduction.'''
    print(f'\n\n{"-" * 80}\n{title}\n{"-" * 80}', end='')

def intro_test(title):
    '''Print a TEST introduction.'''
    print(f'\n\t{title} '.ljust(65, '_'), end='')

def setup_test(browser=False, url='http://ipinfo.io/'):
    '''
    Instantiate a new driver,
    open a browser window, if appropriate, and
    return the driver object.
    '''
    driver = sf.Driver()
    if browser:
        driver.open(config=CONFIG)
        driver.goto(url)
        if not CONFIG['headless']:
            driver.set_window(CONFIG['browser_size'], CONFIG['browser_position'])
    return driver

# Test Plan 1 - Utility Functions
def test_plan01_case001_date_time_functions():
    '''Test utility functions.'''
    intro_plan('Starting test plan 001 - Utility functions')
    intro_test('Test case 001 - Date and time functions')

    driver = setup_test()
    current_date = driver.get_date()
    date_match = re.search('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', current_date)
    assert date_match is not None

    current_time = driver.get_time()
    time_match = re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}$', current_time)
    assert time_match is not None

def test_plan01_case002_make_valid_name():
    '''Test the make_valid_name method.'''
    intro_test('Test case 002 - Make valid name function')
    driver = setup_test()
    test_string = '    Now-is the (time)    '
    result_string = driver.make_valid_name(test_string)
    assert result_string == 'Now_is_the_time'

# Test Plan 2 - Basic Browser Functions
def test_plan02_case001_open_and_close_test_page():
    '''Test opening and closing a browser with the test page.'''
    intro_plan('Starting test plan 002 - Basic browser functions')
    intro_test('Test case 001 - Open and close test page functions')
    driver = setup_test(CONFIG['browser'], CONFIG['test_page'])
    assert driver.browser.title == 'Test Page'
    driver.close()

def test_plan02_case002_find_elements():
    '''Test the .find method.'''
    intro_test('Test case 002 - Find element functions')
    driver = setup_test(CONFIG['browser'], CONFIG['test_page'])

    # Single Element By ID
    element_list = driver.find('id=text01')
    assert isinstance(element_list, driver.web_element)

    # Hidden element
    element_list = driver.find('id=hidden1')
    assert isinstance(element_list, driver.web_element)
    assert not driver.is_element_clickable(element_list)

    # Multiple Elements By Tag Name
    element_list = driver.find('tag=input')
    assert isinstance(element_list, list) and \
           len(element_list) > 1 and \
           isinstance(element_list[0], driver.web_element)

    # Invalid ID
    element_list = driver.find('id=alskdjflkajsldkfjlaksdf')
    assert isinstance(element_list, list) and \
           not element_list

    driver.close()

def test_plan02_case003_is_element_clickable():
    '''Test the .is_element_clickable method.'''
    intro_test('Test case 003 - Is element clickable functions')
    driver = setup_test(CONFIG['browser'], CONFIG['test_page'])

    clickable_element = driver.find('id=text01')
    assert driver.is_element_clickable(clickable_element)

    hidden_element = driver.find('id=hidden1')
    assert not driver.is_element_clickable(hidden_element)

    hidden_element = driver.wait_until_element_clickable('id=hidden3')
    assert driver.is_element_clickable(hidden_element)
    assert not isinstance(hidden_element, list) #driver.WebElement)

    driver.close()

def test_plan02_case004_text_fields():
    '''Test the .find method on text fields.'''
    intro_test('Test case 004 - Text field functions')
    driver = setup_test(CONFIG['browser'], CONFIG['test_page'])
    field_element = driver.find('id=text01')

    # Check initial value
    field_value = driver.is_field_set(field_element)
    assert field_value == 'Double-click me'

    # Set text field
    driver.set_field(field_element, 'Test123')
    field_value = driver.is_field_set(field_element)
    assert field_value == 'Test123'

    # Append to text field
    driver.set_field(field_element, '456', append=True)
    field_value = driver.is_field_set(field_element)
    assert field_value == 'Test123456'

    # Change text field value
    driver.set_field(field_element, '456')
    field_value = driver.is_field_set(field_element)
    assert field_value == '456'

    # Clear text field
    driver.set_field(field_element, '')
    field_value = driver.is_field_set(field_element)
    assert field_value == ''

    driver.close()

def test_plan02_case005_select_fields():
    '''Test the .find method on select fields.'''
    intro_test('Test case 005 - Select field functions')
    driver = setup_test(CONFIG['browser'], CONFIG['test_page'])
    field_element = driver.find('id=select02')

    # Is field not set
    field_value = driver.is_field_set(field_element)
    assert field_value == []

    # Set select field
    driver.set_field(field_element, [1, 3, 4])
    field_value = driver.is_field_set(field_element)
    assert field_value == ['1', '3', '4']

    # Add values to select field
    driver.set_field(field_element, [2, 5], append=True)
    field_value = driver.is_field_set(field_element)
    assert field_value == ['1', '2', '3', '4', '5']

    # Change select field value
    driver.set_field(field_element, [2, 5])
    field_value = driver.is_field_set(field_element)
    assert field_value == ['2', '5']

    # Clear select field
    driver.set_field(field_element, [])
    field_value = driver.is_field_set(field_element)
    assert field_value == []

    driver.close()

def test_plan02_case006_text_area():
    '''Test the .find method on text area fields.'''
    intro_test('Test case 006 - Text area functions')
    driver = setup_test(CONFIG['browser'], CONFIG['test_page'])
    field_element = driver.find('id=textarea01')

    # Check initial value
    field_value = driver.is_field_set(field_element)
    assert field_value == 'Right-click me'

    # Set text field
    driver.set_field(field_element, 'Test123')
    field_value = driver.is_field_set(field_element)
    assert field_value == 'Test123'

    # Append to text field
    driver.set_field(field_element, '456', append=True)
    field_value = driver.is_field_set(field_element)
    assert field_value == 'Test123456'

    # Change text field value
    driver.set_field(field_element, '456')
    field_value = driver.is_field_set(field_element)
    assert field_value == '456'

    # Clear text field
    driver.set_field(field_element, '')
    field_value = driver.is_field_set(field_element)
    assert field_value == ''

    driver.close()

def test_plan02_case007_checkbox():
    '''Test the .find method on checkbox fields.'''
    intro_test('Test case 007 - Checkbox functions')
    driver = setup_test(CONFIG['browser'], CONFIG['test_page'])
    field_locator = 'id=chbox01'
    field_element = driver.find(field_locator)

    # Checkbox is not set
    field_value = driver.is_field_set(field_element)
    assert not field_value

    # Set checkbox
    driver.set_field(field_element, True)
    field_value = driver.is_field_set(field_element)
    assert field_value

    # Clear checkbox
    driver.set_field(field_element, False)
    field_value = driver.is_field_set(field_element)
    assert not field_value

    driver.close()

def test_plan02_case008_radio_buttons():
    '''Test the .find method on radio button fields.'''
    intro_test('Test case 008 - Radio button functions')
    driver = setup_test(CONFIG['browser'], CONFIG['test_page'])
    field_locator = 'name=radio'
    field_element = driver.find(field_locator)

    # Radio is not set
    field_value = driver.is_radio_button_group_set(field_element)
    assert not field_value

    # Set radio button
    field_element[1].click()
    field_value = driver.is_radio_button_group_set(field_element)
    assert field_value == ['Value 1']

    driver.close()

# Test Plan 3 - Advanced Browser Functions
def test_plan03_case001_double_click_and_alert():
    '''Test the .double_click method.'''
    intro_plan('Starting test plan 003 - Advanced features functions')
    intro_test('Test case 001 - Double-click functions')
    driver = setup_test(CONFIG['browser'], CONFIG['test_page'])
    field_locator = 'id=text01'
    field_element = driver.find(field_locator)
    assert driver.double_click(field_element)
    alert_text = driver.check_alert()
    assert alert_text == 'Double-click event'

    driver.close()

def test_plan03_case002_right_click_and_alert():
    '''Test the .right_click method.'''
    intro_test('Test case 002 - Right-click functions')
    driver = setup_test(CONFIG['browser'], CONFIG['test_page'])
    field_locator = 'id=textarea01'
    field_element = driver.find(field_locator)
    assert driver.right_click(field_element)
    alert_text = driver.check_alert()
    assert alert_text == 'Right-click event'

    driver.close()

# End of Test Plans and Cases
def template():
    '''Template Test Function'''
    driver = setup_test(CONFIG['browser'], CONFIG['test_page'])
    # Do Something Here!
    assert 'Condition'
    driver.close()

if __name__ == '__main__':
    print('Do not run this script directly.')
    print(f'Run "pytest -s" from this ({os.path.dirname(os.path.abspath(__file__))}) directory.')
