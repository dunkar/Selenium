#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import unittest
import SeleniumFramework as sf

class TestPlan( unittest.TestCase ):
    def setUp( self ):
        self.driver = sf.Driver()
        self.driver.open()
        
    def tearDown( self ):
        self.driver.close()
        del self.driver

    def test_001_open_url(self):
        d = self.driver
        d.goto('https://duckduckgo.com/')
        self.assertTrue('DuckDuckGo' in d.browser.title)
        
    def test_002_convert_locator_successful(self):
        cl = self.driver.convert_locator
        self.assertTrue(cl('id=abc')        == (self.driver.By.ID, 'abc'))
        self.assertTrue(cl('window=001')    == ('window','001'))
        self.assertTrue(cl('frame=xyz')     == ('frame','xyz'))
        
    def test_003_convert_locator_failure(self):
        cl = self.driver.convert_locator
        self.assertFalse(cl('sound=quack'))

        
if __name__ == '__main__':
    unittest.main( warnings='ignore' )
