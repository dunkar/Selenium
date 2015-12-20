#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Selenium Framework
################################################################################

import os
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

################################################################################
# Module Variables

################################################################################
# Module Classes


class Object(object):
    pass

class FrameworkException(Exception):
    pass

class Driver(object):
    def __init__(self):
        self.WebElement = WebElement
        self.Select = Select
        self.Keys = Keys

    ############################################################################
    # Browser-dependent Methods
    ############################################################################
    def check_alert(self, accept_alert=True):
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

    def control_click(self, webelement, container=None):
        if container is None:
            container = self.browser
        try:
            #AC(container).key_down(Keys.CONTROL).click(webelement).key_up(Keys.CONTROL).perform()
            AC(container)\
                .context_click(webelement)\
                .send_keys(Keys.ARROW_DOWN)\
                .send_keys(Keys.ENTER)\
                .perform()
            self.wait(.5)
            return True
        except:
            return False

    def double_click(self, webelement, container=None):
        if container is None:
            container = self.browser
        try:
            AC(container).double_click(webelement).perform()
            self.wait(.5)
            return True
        except:
            return False

    def find(self, locator_string, container=None, wait=3):
        if not container:
            container = self.browser
        loc_type, loc_value = self.convert_locator(locator_string)
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
        #if not isinstance(webelement, self.WebElement):
        #    return False
        if (webelement.is_displayed() and
            webelement.is_enabled() and
            webelement.size['width'] > 0 and
            webelement.size['height'] > 0
            ):
            return True
        else:
            return False

    def is_field_set(self, webelement):
        try:
            field_tag = webelement.tag_name
            field_type = webelement.get_attribute('type') or None
            if field_tag == 'select':
                field_value_list = Select(webelement).all_selected_options
                field_value = [f.text for f in field_value_list]
            elif field_tag == 'input' and field_type == 'checkbox':
                field_value = webelement.is_selected()
            elif field_tag in [ 'input', 'textarea' ]:
                field_value = webelement.get_attribute('value')
            else:
                field_value = None
        except:
            field_value = None
        return field_value

    def is_radio_button_group_set(self, button_group):
        field_value = [ button.get_attribute('value')
                        for button in button_group
                        if button.is_selected()
                        ]
        return field_value

    def open(self, browser_name='gc', selenium_hub='local', selenium_port='4444'):
        browsers = {
            #local driver name, remote driver capabilities
            'ff': ( 'Firefox', 'FIREFOX'),
            'gc': ( 'Chrome' , 'CHROME'),
            'hu': ( None     , 'HTMLUNITWITHJS'),
            'ie': ( 'Ie'     , 'INTERNETEXPLORER'),
        }
        local_driver, remote_driver = browsers[browser_name]

        # Get the right driver
        if selenium_hub == 'local' and browser_name != 'hu':
            self.browser = getattr(WD, local_driver)()
        elif selenium_hub != 'local':
            command_executor     = 'http://{0}:{1}/wd/hub'.format(selenium_hub, selenium_port)
            desired_capabilities = getattr(WD.DesiredCapabilities, remote_driver)
            self.browser = WD.Remote(
                command_executor        = command_executor,
                desired_capabilities    = desired_capabilities,
                browser_profile         = None
                )
        else:
            raise 'Invalid browser selection.'

        # Setup the driver close method
        if selenium_hub == 'local' and browser_name == 'gc':
            self.close      = self.browser.quit
        else:
            self.close      = self.browser.close

    def right_click(self, webelement, container=None):
        if container is None:
            container = self.browser
        try:
            AC(container).context_click(webelement).perform()
            self.wait(.5)
            return True
        except:
            return False

    def scroll_into_view(self, webelement):
        self.browser.execute_script("arguments[0].scrollIntoView(true);", webelement)
        self.wait(.5)

    def set_field(self, webelement, field_value, append=False):
        field_tag = webelement.tag_name
        if field_tag == 'textarea' or \
            (field_tag == 'input' and \
            webelement.get_attribute('type') not in ['radio','checkbox']
            ):
                webelement.click()
                if not append:
                    webelement.clear()
                webelement.send_keys(field_value)
                #self.find('tag=body').click()
        elif field_tag == 'input':
            webelement.click()
        elif field_tag == 'select':
            select_element = Select(webelement)
            if not append:
                select_element.deselect_all()
            if isinstance(field_value, list):
                [select_element.select_by_visible_text(str(item))
                    for item in field_value
                    ]
            elif isinstance(field_value, str):
                select_element.select_by_visible_text(field_value)

    def set_window(self, window_size, window_position):
        self.browser.set_window_size(window_size[0], window_size[1])
        self.browser.set_window_position(window_position[0], window_position[1])

    def switch_to(self, locator_string=None, container=None):
        if container is None:
            container = self.browser
        if locator_string is not None:
            locator_type, locator_value = self.convert_locator(locator_string)
        else:
            locator_type = None
        if locator_type in [None, '', 'top', 'default']:
            self.browser.switch_to.default_content()
        elif locator_type == 'window':
            container.switch_to.window(locator_value)
        elif locator_type == 'frame':
            container.switch_to.frame(locator_value)
        else:
            raise 'Invalid switch-to target'

    def wait_until_element_clickable(self, locator_string=None, timeout=30):
        locator_object = self.convert_locator(locator_string)
        webelement = WebDriverWait(self.browser, timeout).until(
            EC.element_to_be_clickable(locator_object)
            )
        return webelement


    ############################################################################
    # Browser-independent Utilities
    ############################################################################
    def convert_locator(self, locator_string):
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
        #ut_test_001
        return self.get_timestamp()[:10]

    def get_time(self):
        # ut_test_002
        return self.get_timestamp()[-8:]

    def get_timestamp(self):
        return str(datetime.now())[:-7]

    def make_valid_name(self, invalid_name):
        tmp_name = invalid_name.strip()
        tmp_name = re.sub('[ -]', '_', tmp_name)
        tmp_name = re.sub('[()]', '', tmp_name)
        return tmp_name

    def pause(self, message_text=None):
        if message_text:
            print(message_text)
        input('Press the ENTER key to continue.')

    def wait(self, seconds=0):
        time.sleep(seconds)

    def throw(self, message):
        raise FrameworkException(message)


if __name__ == '__main__':
    print('The Selenium Framework module is not intended to run \
           as a script.')
    print('Add the following line to your scripts or type this in your \
           Python session:')
    print('\timport SeleniumFramework as sf')
