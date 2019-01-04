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
# Inputs and variables:
browser          = 'gc'                        # Can be gc, ff, ie.
test_url         = 'https://duckduckgo.com/'   # Starting URL.
identifier_type  = 'name'                      # Can be any css identifier like id, tag, name, etc.
identifier_value = 'q'                         # Value associated with the identifier listed above.
search_string    = 'SeleniumHQ'                # Test criteria

# Execute steps:
import SeleniumFramework as SF
driver = SF.Driver()
driver.open(browser) 
driver.goto(test_url)
element = driver.find(f'{identifier_type}={identifier_value}') 
    # By default, the driver.find method tries two times with a 3-second delay between attempts.
element.send_keys(search_string)
element.submit()
assert driver.browser.title == f'{search_string} at DuckDuckGo'
driver.close()
```
