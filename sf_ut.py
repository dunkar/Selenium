#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import unittest
import SeleniumFramework as sf

class TestPlan( unittest.TestCase ):
    def setUp( self ):
        self.driver = sf.Driver()
        
    def tearDown( self ):
        del self.driver

    def test_001_open_close_browser(self):
        self.assertTrue(False)
        
    def test_002_navigate_to_webpage(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main( warnings='ignore' )
