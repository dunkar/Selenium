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
        self.assertEqual(cl('id=abc'),      (self.driver.By.ID, 'abc'))
        self.assertEqual(cl('window=001'),  ('window','001'))
        self.assertEqual(cl('frame=xyz'),   ('frame','xyz'))

    def test_003_convert_locator_failure(self):
        cl = self.driver.convert_locator
        self.assertFalse(cl('sound=quack'))
        self.assertFalse(cl('quack'))
        self.assertFalse(cl(1))

    def test_004_find_element(self):
        search_text = 'Hello World'
        d = self.driver
        d.goto('https://duckduckgo.com/')
        el = d.find('name=q')[0]
        el.send_keys(search_text)
        fm = d.find('tag=form')[0]
        fm.submit()
        self.assertTrue(search_text in d.browser.title)
        [print(link.text)
            for link in d.find('tag=a')
            if search_text in link.text
            ]


if __name__ == '__main__':
    unittest.main( warnings='ignore' )
