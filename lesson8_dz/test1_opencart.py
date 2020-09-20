from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# Opencart

def test_example1(browser, url, wait):
    browser.get(url)
    element = browser.find_element_by_css_selector('footer p a')
    element.send_keys(Keys.END)
    element_url = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="http://www.opencart.com"]')))
    assert element_url.text == 'OpenCart'
