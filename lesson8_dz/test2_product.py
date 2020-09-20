import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


# Карточка товара /index.php?route=product/product&path=57&product_id=49

# 1. Проверка, что находимся на карточке товара Samsung Galaxy Tab 10.1
@pytest.mark.parametrize("product_id", [49])
def test_catalog_name(browser, url, product_id):
    product_url = url + f'/index.php?route=product/product&path=57&product_id=' + str(product_id)
    browser.get(product_url)
    product_name = browser.find_element_by_css_selector('#content h2').text
    assert product_name == 'Samsung Galaxy Tab 10.1'


# 2. Проверка цены товара
@pytest.mark.parametrize("product_id", [49])
def test_catalog_name(browser, url, product_id):
    product_url = url + f'/index.php?route=product/product&path=57&product_id=' + str(product_id)
    browser.get(product_url)
    element = browser.find_elements_by_css_selector('.product-layout')[product_id]
    price = str(element.find_element_by_css_selector('.product-layout .price').text)
    name = element.find_element_by_css_selector('.product-layout .caption a')
    name.click()
    page = browser.find_element_by_css_selector('#content .row .col-sm-4 h2')
    assert page.text == price

# 3. Gроверка добавления в wish list
@pytest.mark.parametrize("product_id", [40, 30, 36, 49])
def test_add_wish_list(browser, url, product_id, wait):
    product_page_url = url + f'/index.php?route=product/product&path=57&product_id=' + str(product_id)
    browser.get(product_page_url)
    product_name = browser.find_element_by_css_selector('#content .col-sm-4 h1').text
    wish_list_button = browser.find_element_by_css_selector('[data-original-title="Add to Wish List"]')
    wish_list_button.click()
    alert = wait.until((EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-success'))))
    alert.find_element_by_link_text('login').click()
    browser.find_element_by_css_selector('#input-email').send_keys('test404@mail.ru')
    browser.find_element_by_css_selector('#input-password').send_keys('test')
    browser.find_element_by_css_selector('input[value=Login]').click()
    browser.find_element_by_link_text('Wish List').click()
    wish_list_product_name = browser.find_element_by_link_text(product_name).text
    assert wish_list_product_name == product_name


# 4. Проверка добавления в Cart
@pytest.mark.parametrize("product_id", [47, 40, 30, 36, 49])
def test_add_cart(browser, url, product_id, wait):
    product_page_url = url + f'/index.php?route=product/product&path=57&product_id=' + str(product_id)
    browser.get(product_page_url)
    product_name = browser.find_element_by_css_selector('#content .col-sm-4 h1').text
    select = browser.find_elements_by_tag_name('select')
    if len(select) != 0:
        select = Select(select[0])
        select.select_by_index(1)
    cart_button = browser.find_element_by_css_selector('#button-cart')
    cart_button.click()
    alert = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-success')))
    alert.find_element_by_link_text('shopping cart').click()
    cart_product_name = browser.find_element_by_link_text(product_name).text
    assert cart_product_name == product_name


# 5. Тест написания ревью
@pytest.mark.parametrize("product_id", [47, 40, 30, 36, 49])
def test_review(browser, url, product_id, wait):
    product_page_url = url + f'/index.php?route=product/product&path=57&product_id=' + str(product_id)
    browser.get(product_page_url)
    time.sleep(3)
    reviews = browser.find_element_by_css_selector('.nav-tabs').find_element_by_partial_link_text('Reviews')
    reviews.click()
    reviews_name = browser.find_element_by_css_selector('#input-name')
    reviews_name.send_keys('Test Test')
    reviews_text = browser.find_element_by_css_selector('#input-review')
    reviews_text.send_keys('It is really good product. Test Test Test Test Test Test Test Test Test Test Test')
    rating = browser.find_elements_by_css_selector("[name='rating']")
    rating[4].click()
    browser.find_element_by_css_selector('.pull-right #button-review').send_keys(Keys.END)
    button = browser.find_element_by_css_selector('.pull-right #button-review')
    button.click()
    alert = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-success')))
    alert_text = str(alert.text)
    alert_text_thank = alert_text.split('.')[0]
    assert alert_text_thank == 'Thank you for your review'