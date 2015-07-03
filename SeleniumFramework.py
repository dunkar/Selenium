#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import time
import os
from datetime                                   import datetime
from selenium                                   import webdriver
from selenium.webdriver.common.action_chains    import ActionChains
from selenium.webdriver.common.by               import By
from selenium.webdriver.common.keys             import Keys
from selenium.webdriver.support                 import expected_conditions
from selenium.webdriver.support.ui              import Select
from selenium.webdriver.support.ui              import WebDriverWait
from selenium.webdriver.remote.webelement       import WebElement
from selenium.webdriver.remote.webdriver        import WebDriver
from selenium.common                            import exceptions
from selenium.common.exceptions                 import NoSuchElementException
from selenium.common.exceptions                 import NoAlertPresentException
from selenium.common.exceptions                 import TimeoutException


class Driver(object):
    def __init__(self):
        self.AC = ActionChains
        self.By = By
        self.EC = expected_conditions
        self.EX = exceptions
        self.Keys = Keys
        self.Select = Select
        self.WD = webdriver
        self.WDWait = WebDriverWait
        self.WebElement = WebElement
        self.WebDriver = WebDriver
        
    def open(self):
        pass
        
    def close(self):
        pass
        
    
class Object( object ):
    pass


if __name__ == '__main__':
    print('The Selenium Framework is not intended to run as a script.')
    print('Add the following line to your scripts or type this in your Python session:')
    print('\timport SeleniumFramework as sf')
        
