# Selenium

Purpose: To build a framework around the Selenium WebDriver to simplify the
basic capabilities that are most frequently used (in my experience anyway).

# Instructions
- Install Python version 3
- Install the selenium bindings for Python: `pip install selenium`
- Install the SeleniumFramework.py file into a location searchable by Python
    - i.e. site-packages or the folder containing your test scripts
- Sample test script:

```
import SeleniumFramework as SF
d = SF.Driver()
d.open('gc') # Can be gc, ff, ie
d.goto('https://duckduckgo.com/')
el = d.find('name=q')
el.send_keys('SeleniumHQ')
el.submit()
assert d.browser.title == 'SeleniumHQ at DuckDuckGo'
d.close()
```
