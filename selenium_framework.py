#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
A framework built around the Selenium WebDriver to simplify the basic capabilities that are
most frequently used (in my experience anyway).
'''
################################################################################
# Selenium Framework
__title__ = 'Selenium Framework'
__version__ = '0.5.0'
__copyright__ = '2011 - 2020'
__author__ = 'John Dahl'
__date__ = '2020-02-08'
__license__ = '''MIT License

Copyright (c) 2011-2020 John Dahl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''
################################################################################

import re
import time

from datetime                                   import datetime

from selenium                                   import webdriver as WD
from selenium.webdriver.common.action_chains    import ActionChains as AC
from selenium.webdriver.common.by               import By
from selenium.webdriver.common.keys             import Keys
from selenium.webdriver.support                 import expected_conditions as EC
from selenium.webdriver.support.ui              import Select
from selenium.webdriver.support.ui              import WebDriverWait
from selenium.webdriver.remote.webelement       import WebElement
from selenium.common.exceptions                 import NoAlertPresentException
from selenium.common.exceptions                 import TimeoutException
# from selenium.webdriver.remote.webdriver        import WebDriver
# from selenium.common                            import exceptions as EX
# from selenium.common.exceptions                 import NoSuchElementException
from selenium.common.exceptions                 import WebDriverException

class FrameworkException(WebDriverException):
    '''Framework exception for deliberately thrown exceptions.'''
    # pass

class Driver():
    '''
    Main framework object. Everything runs from an instance of this object.
    '''
    def __init__(self):
        self.browser = None
        self.close = None
        self.web_element = WebElement
        self.keys = Keys

    ############################################################################
    # Browser-dependent Methods
    ############################################################################
    def check_alert(self, accept_alert=True):
        '''Given that this method is called when a browser alert is present,
        retrieve the message in the alert,
        take the action requested (accept by default), and
        return the message.'''
        try:
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            if accept_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        except NoAlertPresentException:
            return False
        except WebDriverException:
            self.throw(f'Unable to check the alert.')

    def control_click(self, webelement, container=None):
        '''Given a web element,
        perform a control-click on the element and
        return a boolean confirmation of the success of the action.'''
        if container is None:
            container = self.browser
        try:
            AC(container)\
                .context_click(webelement)\
                .send_keys(Keys.ARROW_DOWN)\
                .send_keys(Keys.ENTER)\
                .perform()
            self.wait(.5)
            return True
        except WebDriverException:
            return False

    def double_click(self, webelement, container=None):
        '''Given a web element,
        perform a double-click on the element and
        return a boolean confirmation of the success of the action.'''
        if container is None:
            container = self.browser
        try:
            AC(container).double_click(webelement).perform()
            self.wait(.5)
            return True
        except WebDriverException:
            return False

    def find(self, locator_string, container=None, wait=3):
        '''Given a locator in the form of "type=value",
        an optional container within which to start a nested search,
        and an optional wait time,
        locate the elements and return a list of results.
        If a result is not found, a second attempt will be made after
        the wait time.
        If the search returns a single result, that result is returned
        from the method as a WebElement.'''
        if not container:
            container = self.browser
        loc_type, loc_value = self._convert_locator(locator_string)
        try:
            element_list = container.find_elements(by=loc_type, value=loc_value)
            if (not element_list and isinstance(wait, int) and wait > 0):
                WebDriverWait(self.browser, wait).until(
                    EC.presence_of_element_located((loc_type, loc_value))
                )
                element_list = container.find_elements(by=loc_type, value=loc_value)
            if len(element_list) == 1:
                element_list = element_list[0]
        except TimeoutException:
            element_list = []
        return element_list

    def goto(self, url):
        '''Navigate to the given url.'''
        self.browser.get(url)

    def is_element_clickable(self, webelement):
        '''Given a web element, determine if it is eligable to click on it.'''
        #if not isinstance(webelement, WebElement):
        #    return False
        if (webelement.is_displayed() and
                webelement.is_enabled() and
                webelement.size['width'] > 0 and
                webelement.size['height'] > 0):
            return True
        else:
            return False

    def is_field_set(self, webelement):
        '''Given a web element representing a form field,
        determine if the field has a value set, and if so,
        return the value or None.'''
        try:
            field_tag = webelement.tag_name
            field_type = webelement.get_attribute('type') or None
            if field_tag == 'select':
                field_value_list = Select(webelement).all_selected_options
                field_value = [f.text for f in field_value_list]
            elif field_tag == 'input' and field_type in ['checkbox', 'radio']:
                field_value = webelement.is_selected()
            elif field_tag in ['input', 'textarea']:
                field_value = webelement.get_attribute('value')
            else:
                field_value = None
        except WebDriverException:
            field_value = None
        return field_value

    def is_radio_button_group_set(self, button_group):
        '''Given a web element representing a radio button group,
        determine if the field has a value set, and if so,
        return the value or None.'''
        field_value = [button.get_attribute('value')
                       for button in button_group
                       if button.is_selected()]
        return field_value

    def open(self, config=None):
        '''
        Open a new instance of the selected browser and
        set the close method.
        TODO: Add custom profile support.
        TODO: Add remote/grid support.
        '''
        if not config:
            browser = input('Which browser would you like to use: ').capitalize()
            headless = True
        else:
            browser = config['browser']
            headless = config['headless']

        if browser == 'Chrome':
            options = WD.chrome.options.Options()
            if headless:
                options.add_argument("--headless")
                options.add_argument("--window-size=1920x1080")
        elif browser == 'Firefox':
            options = WD.firefox.options.Options()
            options.headless = headless

        # Remote
        # if config.get('remote_hub', False):
        #     url, port = config['remote_hub']
        #     if browser_name == 'Ie':
        #         browser_name = 'INTERNETEXPLORER'
        #     else:
        #         browser_name = browser_name.upper()
        #     self.browser = WD.Remote(
        #         command_executor=f'http://{url}:{port}/wd/hub',
        #         desired_capabilities=getattr(WD.DesiredCapabilities, browser_name),
        #         browser_profile=browser_options['profile'])

        try:
            self.browser = getattr(WD, browser)(options=options)
            self.close = self.browser.close
        except IndexError:
            self.throw('Unknown browser selected.')

    # def open_bak(self, browser_name='gc', selenium_hub='local', selenium_port='4444'):
    #     elif selenium_hub != 'local':
    #         command_executor = 'http://{0}:{1}/wd/hub'.format(selenium_hub, selenium_port)
    #         desired_capabilities = getattr(WD.DesiredCapabilities, remote_driver)
    #         self.browser = WD.Remote(
    #             command_executor=command_executor,
    #             desired_capabilities=desired_capabilities,
    #             browser_profile=None)
    #     else:
    #         raise 'Invalid browser selection.'
    #    # Setup the driver close method

    def right_click(self, webelement, container=None):
        '''Given a web element, right-click on it.'''
        if container is None:
            container = self.browser
        try:
            AC(container).context_click(webelement).perform()
            self.wait(.5)
            return True
        except WebDriverException:
            return False

    def scroll_into_view(self, webelement):
        '''Given a web element on the current page,
        scroll the page until the element is visible.'''
        self.browser.execute_script("arguments[0].scrollIntoView(true);", webelement)
        self.wait(.5)

    def set_field(self, webelement, field_value, append=False):
        '''Given a form field, set the value of the field.'''
        field_tag = webelement.tag_name
        if field_tag == 'textarea' or \
            field_tag == 'input' and \
            webelement.get_attribute('type') not in ['radio', 'checkbox']:
            webelement.click()
            if not append:
                webelement.clear()
            webelement.send_keys(field_value)
            #self.find('tag=body').click()
        elif field_tag == 'input':
            webelement.click()
        elif field_tag == 'select':
            select_element = Select(webelement)
            if isinstance(field_value, str):
                select_element.select_by_visible_text(field_value)
            elif isinstance(field_value, list):
                if (len(field_value) > 1 and not append) or not field_value:
                    select_element.deselect_all()
                for item in field_value:
                    select_element.select_by_visible_text(str(item))

    def set_window(self, window_size, window_position):
        '''Set the browser window size and position.'''
        self.browser.set_window_size(window_size[0], window_size[1])
        self.browser.set_window_position(window_position[0], window_position[1])

    def switch_to(self, locator_string=None, container=None):
        '''Change the browser context to a different window or frame.'''
        try:
            if container is None:
                container = self.browser
            if locator_string is not None:
                locator_type, locator_value = self._convert_locator(locator_string)
            else:
                locator_type = None
            if locator_type in [None, '', 'top', 'default']:
                self.browser.switch_to.default_content()
            elif locator_type == 'window':
                container.switch_to.window(locator_value)
            elif locator_type == 'frame':
                container.switch_to.frame(locator_value)
            else:
                self.throw(f'Invalid switch-to target: {locator_string}')
        except WebDriverException:
            self.throw(f'Unable to swtich to the target: {locator_string}')

    def wait_until_element_clickable(self, locator_string=None, timeout=30):
        '''Wait until the condition exists when the element is clickable or timeout.'''
        locator_object = self._convert_locator(locator_string)
        webelement = WebDriverWait(self.browser, timeout).until(
            EC.element_to_be_clickable(locator_object))
        return webelement


    ############################################################################
    # Browser-independent Utilities
    ############################################################################
    def _convert_locator(self, locator_string):
        '''Given a locator string in the format type=value
        return a tuple in the format (valid_type, value)'''
        locator_map = {
            'id'    : By.ID,
            'name'  : By.NAME,
            'css'   : By.CSS_SELECTOR,
            'class' : By.CLASS_NAME,
            'link'  : By.LINK_TEXT,
            'plink' : By.PARTIAL_LINK_TEXT,
            'tag'   : By.TAG_NAME,
            'xpath' : By.XPATH,
            'window': 'window',
            'frame' : 'frame',
        }
        locator_string_separator = locator_string.find('=')
        locator_type = locator_string[:locator_string_separator].strip()
        locator_value = locator_string[locator_string_separator + 1:].strip()
        return (locator_map[locator_type], locator_value)

    def get_date(self):
        '''Return the current date.'''
        #ut_test_001
        return self.get_timestamp()[:10]

    def get_time(self):
        '''Return the current time.'''
        # ut_test_002
        return self.get_timestamp()[-8:]

    def get_timestamp(self):
        '''Return the current datetime.'''
        return str(datetime.now())[:-7]

    def make_valid_name(self, invalid_name):
        '''Remove bad characters and return a valid name.'''
        tmp_name = invalid_name.strip()
        tmp_name = re.sub('[ -]', '_', tmp_name)
        tmp_name = re.sub('[()]', '', tmp_name)
        return tmp_name

    def pause(self, message_text=None):
        '''Pause the current execution until the Enter key is pressed.'''
        if message_text:
            print(message_text)
        input('Press the ENTER key to continue.')

    def wait(self, seconds=0):
        '''Pause the current execution for the given number of seconds.'''
        time.sleep(seconds)

    def throw(self, message):
        '''Raise a FrameworkException error.'''
        raise FrameworkException(message)


if __name__ == '__main__':
    print('The Selenium Framework module is not intended to run \
           as a script.')
    print('Add the following line to your scripts or type this in your \
           Python session:')
    print('\timport selenium_framework as sf')
