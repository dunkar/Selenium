#!/usr/bin/env python

import SeleniumFramework as sf
import config

d = sf.Driver()
def cb():
    d.close()
    exit()
d.open(
    browser_name=config.browser_name,
    selenium_hub=config.selenium_hub,
    selenium_port=config.selenium_port
    )
d.goto(config.test_page)
