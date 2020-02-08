# Selenium Framework

Purpose: To build a framework around the Selenium WebDriver to simplify the
basic capabilities that are most frequently used (in my experience anyway).

## Instructions
- Install Python version 3
- Install the selenium bindings for Python: `pip install selenium`
- Install the selenium_framework.py file into a location searchable by Python
    - i.e. site-packages or the folder containing your project scripts


## Sample:
```
import selenium_framework as sf

CONFIG = {
    'browser': 'Chrome',
    'headless': True,
    'browser_size': (800, 600),
    'browser_position': (0, 0),
    'test_page': f'https://duckduckgo.com/'
}

driver = sf.Driver()
driver.open(CONFIG)
driver.goto(CONFIG['test_page'])

element = driver.find('name=q') 
element.send_keys('SeleniumHQ')
element.submit()

assert driver.browser.title == 'SeleniumHQ at DuckDuckGo'
driver.close()
```

# Links
[Selenium Website](https://seleniumhq.dev/)  
[Selenium Repo](https://github.com/seleniumhq/selenium)  

[Python API Documentation](https://selenium.dev/selenium/docs/api/py/index.html) 

[Browser Drivers](https://selenium.dev/documentation/en/webdriver/driver_requirements/#quick-reference)  

[Firefox Gecko Driver Documentation](https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html)  
[Firefox Gecko Driver repo](https://github.com/mozilla/geckodriver/releases)  

[Google Chrome Driver](https://chromedriver.storage.googleapis.com/index.html)
