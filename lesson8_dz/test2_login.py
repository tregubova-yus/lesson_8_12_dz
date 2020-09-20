from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Страницу логина /index.php?route=account/login

def test_login_user(browser, url, wait):
    login_page_url = url + f'/index.php?route=account/login'
    browser.get(login_page_url)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.well form')))
    browser.find_element_by_css_selector('#input-email').send_keys('test123@mail.ru')
    browser.find_element_by_css_selector('#input-password').send_keys('test')
    browser.find_element_by_css_selector('input[value=Login]').click()
    browser.find_element_by_link_text('Edit Account').click()
    login_user_email = browser.execute_script('return document.getElementById("input-email").value;')
    assert login_user_email == 'test123@mail.ru'


def test_register_user(browser, url, wait):
    login_page_url = url + f'/index.php?route=account/login'
    browser.get(login_page_url)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.well a')))
    browser.find_element_by_link_text('Continue').click()
    browser.find_element_by_css_selector('#input-email').send_keys('test123@mail.ru')
    browser.find_element_by_css_selector('#input-telephone').send_keys('+79999999999')
    browser.find_element_by_css_selector('#input-firstname').send_keys('Test')
    browser.find_element_by_css_selector('#input-lastname').send_keys('Test')
    browser.find_element_by_css_selector('#input-password').send_keys('test')
    browser.find_element_by_css_selector('#input-confirm').send_keys('test')
    browser.find_element_by_css_selector('[type="checkbox"]').click()
    browser.find_element_by_css_selector('[type="submit"]').click()
    alert_danger = browser.find_element_by_css_selector('.alert-danger').text
    assert alert_danger == 'Warning: E-Mail Address is already registered!'