import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import operator
from functools import reduce
import math


# Opencart. Главная страница
# 1. Открываем карточку с товаром по названию MacBook во Featured
def test_open_product_neme(browser, url, wait):
    browser.get(url)
    element = browser.find_elements_by_css_selector('.product-layout .product-thumb')[0]
    actions = ActionChains(browser)
    actions.move_to_element(element)
    name_element = browser.find_element_by_css_selector('.product-layout .caption a').text
    actions.perform()
    element.click()
    product_name = browser.find_element_by_css_selector('#content .col-sm-4 h1')
    assert product_name.text == name_element


# 2. Открываем карточку с товаром по картинке
def test_open_product(browser, url):
    browser.get(url)
    element = browser.find_element_by_css_selector('.product-layout .img-responsive')
    actions = ActionChains(browser)
    actions.move_to_element(element)
    name_element = browser.find_element_by_css_selector('.product-layout .caption a').text
    actions.perform()
    element.click()
    page = browser.find_element_by_css_selector('#content .col-sm-4 h1')
    assert page.text == name_element


# 3. Переход на информацию About Us
def test_click_information(browser, url):
    browser.get(url)
    browser.find_element_by_css_selector('body footer div div div:nth-child(1) ul li:nth-child(1) a').send_keys(Keys.END)
    element = browser.find_element_by_css_selector('body footer div div div:nth-child(1) ul li:nth-child(1) a')
    element.click()
    page = browser.find_element_by_css_selector('#content h1')
    assert page.text == 'About Us'


# 4. Проверяем стоимость товаров во Featured
@pytest.mark.parametrize("product_index", [0, 1, 2, 3])
def test_price(browser, url, product_index):
    browser.get(url)
    element = browser.find_elements_by_css_selector('.product-layout')[product_index]
    # element.location_once_scrolled_into_view
    price = str(element.find_element_by_css_selector('.product-layout .price').text)
    name = element.find_element_by_css_selector('.product-layout .caption a')
    name.click()
    page = browser.find_element_by_css_selector('#content .row .col-sm-4 h2')
    assert page.text == price


# 5. Пролистывание картинок на главной странице по горизонтальному переключателю
def test_picture(browser, url, wait):
    browser.get(url)
    picture_first = browser.find_element_by_css_selector('.swiper-viewport #slideshow0')
    picture_first.screenshot('pic_1.png')
    bullet = browser.find_element_by_css_selector('#content .swiper-pagination-bullet')
    bullet.click()
    picture_second = browser.find_element_by_css_selector('.swiper-viewport #slideshow0')
    picture_second.screenshot('pic_2.png')
    pic1 = Image.open('pic_1.png').histogram()
    pic2 = Image.open('pic_2.png').histogram()
    test = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, pic1, pic2)) / len(pic1))
    if test <= 90:
        diff = "equal"
    else:
        diff = "not equal"
    assert diff == 'not equal'
