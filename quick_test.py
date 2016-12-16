#!/usr/bin/env python
# Quick test script for the Selenium Framework module.

import re
import unittest
import SeleniumFramework as sf

browser_name='gc'
test_page = 'http://localhost:8000/test_page.html'

d = sf.Driver()

# Check utility methods
current_date = d.get_date()
date_match = re.search('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', current_date)
assert(date_match is not None)

current_time = d.get_time()
time_match = re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}$', current_time)
assert(time_match is not None)

test_string = '    Now-is the (time)    '
result_string = d.make_valid_name(test_string)
assert(result_string == 'Now_is_the_time')

# Open a browser window and navigate to the test page
d.open(browser_name)
d.set_window((1024, 768), (50, 20))
d.goto(test_page)
assert(d.browser.title == 'Test Page')

# Find elements:
element_list = d.find('id=text01')
assert(isinstance(element_list, d.WebElement))

element_list = d.find('id=hidden1')
assert(isinstance(element_list, d.WebElement))
assert(not d.is_element_clickable(element_list))

element_list = d.find('tag=input')
assert(
    isinstance(element_list, list) and
    len(element_list) > 1 and
    isinstance(element_list[0], d.WebElement)
    )

element_list = d.find('id=alskdjflkajsldkfjlaksdf')
assert(
    isinstance(element_list, list) and
    len(element_list) == 0
    )

# Check if elements are clickable:
clickable_element = d.find('id=text01')
assert(d.is_element_clickable(clickable_element))

clickable_element = d.find('id=out_of_view')
assert(d.is_element_clickable(clickable_element))

hidden_element = d.find('id=hidden1')
assert(not d.is_element_clickable(hidden_element))

hidden_element = d.wait_until_element_clickable('id=hidden2')
assert(d.is_element_clickable(hidden_element))
assert(isinstance(hidden_element, d.WebElement))

# Check input/text fields:
field_element = d.find('id=text01')

field_value = d.is_field_set(field_element)
assert(not field_value)

d.set_field(field_element, 'Test123')
field_value = d.is_field_set(field_element)
assert(field_value == 'Test123')

d.set_field(field_element, '456', append=True)
field_value = d.is_field_set(field_element)
assert(field_value == 'Test123456')

d.set_field(field_element, '456')
field_value = d.is_field_set(field_element)
assert(field_value == '456')

d.set_field(field_element, '')
field_value = d.is_field_set(field_element)
assert(field_value == '')

# Check text area fields:
field_element = d.find('id=textarea01')

field_value = d.is_field_set(field_element)
assert(not field_value)

d.set_field(field_element, 'Test123')
field_value = d.is_field_set(field_element)
assert(field_value == 'Test123')

d.set_field(field_element, '456', append=True)
field_value = d.is_field_set(field_element)
assert(field_value == 'Test123456')

d.set_field(field_element, '456')
field_value = d.is_field_set(field_element)
assert(field_value == '456')

d.set_field(field_element, '')
field_value = d.is_field_set(field_element)
assert(field_value == '')

# Check checkbox fields:
field_locator = 'id=chbox01'
field_element = d.find(field_locator)

field_value = d.is_field_set(field_element)
assert(not field_value)

d.set_field(field_element, True)
field_value = d.is_field_set(field_element)
assert(field_value)

d.set_field(field_element, False)
field_value = d.is_field_set(field_element)
assert(not field_value)

# Check radio button fields:
field_locator = 'name=radio'
field_element = d.find(field_locator)

field_value = d.is_radio_button_group_set(field_element)
assert(not field_value)

field_element[1].click()
field_value = d.is_radio_button_group_set(field_element)
assert(field_value == ['Value 1'])

field_element[2].click()
field_value = d.is_radio_button_group_set(field_element)
assert(field_value == ['Value 2'])

field_element = d.find('id=radio01')
field_value = d.is_field_set(field_element)
assert(field_value == False)

field_element = d.find('id=radio02')
field_value = d.is_field_set(field_element)
assert(field_value == True)

# Check select fields:
field_element = d.find('id=select01')   # Single Select

field_value = d.is_field_set(field_element)
assert(field_value == ['1'])

d.set_field(field_element, [3])
field_value = d.is_field_set(field_element)
assert(field_value == ['3'])

d.set_field(field_element, [1])
field_value = d.is_field_set(field_element)
assert(field_value == ['1'])

field_element = d.find('id=select02')   # Multi-select

field_value = d.is_field_set(field_element)
assert(field_value == [])

d.set_field(field_element, [1, 3, 4])
field_value = d.is_field_set(field_element)
assert(field_value == ['1', '3', '4'])

d.set_field(field_element, [2, 5], append=True)
field_value = d.is_field_set(field_element)
assert(field_value == ['1', '2', '3', '4', '5'])

d.set_field(field_element, [2, 5])
field_value = d.is_field_set(field_element)
assert(field_value == ['2', '5'])

d.set_field(field_element, [])
field_value = d.is_field_set(field_element)
assert(field_value == [])

# Check Advanced Functions:
field_element = d.find('id=text01')
assert(d.double_click(field_element))
alert_text = d.check_alert()
assert(alert_text == 'Double-click event')

field_element = d.find('id=chbox01')
assert(d.right_click(field_element))
alert_text = d.check_alert()
assert(alert_text == 'Right-click event')

d.close()
