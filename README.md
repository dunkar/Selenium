# Selenium

Purpose: To build a framework around the Selenium WebDriver to simplify the
basic capabilities that are most frequently used (in my experience anyway).

# Instructions
- Install Python version 3
- Install the selenium bindings for Python: `pip install selenium`
- Install the selenium_framework.py file into a location searchable by Python
    - i.e. site-packages or the folder containing your test scripts
- Sample test script:
```
import selenium_framework as sf

driver = sf.Driver()
driver.open('gc')   # Can be js, gc, ff, ie.
driver.goto('https://duckduckgo.com/')

element = driver.find('name=q') 
element.send_keys('SeleniumHQ')
element.submit()

assert driver.browser.title == 'SeleniumHQ at DuckDuckGo'
driver.close()
```

# Links
[SeleniumHQ Website](https://seleniumhq.dev/)  
[Selenium Repo](https://github.com/seleniumhq/selenium)  

[Python API Documentation](https://selenium.dev/selenium/docs/api/py/index.html) 
 
[Firefox Gecko Driver Documentation](https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html)  
[Firefox Gecko Driver repo](https://github.com/mozilla/geckodriver/releases)  

