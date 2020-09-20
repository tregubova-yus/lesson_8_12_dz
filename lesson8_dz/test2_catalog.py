import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Тест Каталог /index.php?route=product/category&path=20

# 1. Проверка, что находимся на странице Каталога Desktops
@pytest.mark.parametrize("catalog_id", [20])
def test_catalog_name(browser, url, catalog_id):
    catalog_url = url + f'/index.php?route=product/category&path=' + str(catalog_id)
    browser.get(catalog_url)
    catalog_name = browser.find_element_by_css_selector('#content h2').text
    assert catalog_name == 'Desktops'


# 2. Проверка названий товаров
@pytest.mark.parametrize("catalog_id", [20], [42])
def test_product_name(browser, url, catalog_id, product_id):
    catalog_url = url + f'/index.php?route=product/category&path=' + str(catalog_id) + f'&product_id=' + str(product_id)
    browser.get(catalog_url)
    product_name = browser.find_element_by_css_selector('#content h4').text
    assert product_name == 'Apple Cinema 30"'

# 3. Проверка открытия карточки товара по картинке и по названию
@pytest.mark.parametrize("catalog_id", [20], [42])
def test_product_name(browser, url, catalog_id, product_id):
    catalog_url = url + f'/index.php?route=product/category&path=' + str(catalog_id) + f'&product_id=' + str(product_id)
    browser.get(catalog_url)
    element = browser.find_elements_by_css_selector('.product-layout .product-thumb')[0]
    actions = ActionChains(browser)
    actions.move_to_element(element)
    name_element = browser.find_element_by_css_selector('.product-layout .caption a').text
    actions.perform()
    element.click()
    product_name_name = browser.find_element_by_css_selector('#content .col-sm-4 h1')
    element2 = browser.find_element_by_css_selector('.product-layout .img-responsive')
    actions2 = ActionChains(browser)
    actions2.move_to_element(element)
    name_element2 = browser.find_element_by_css_selector('.product-layout .caption a').text
    actions2.perform()
    element2.click()
    product_name_pic = browser.find_element_by_css_selector('#content .col-sm-4 h1')
    assert name_element2 == product_name_pic


# 4. Проверка добавления товара в wish list
@pytest.mark.parametrize("product_index", [1, 5, 11])
def test_add_to_shopping_cart(browser, url, product_index, wait):
    catalog_url = url + f'/index.php?route=product/category&path=20'
    browser.get(catalog_url)
    product_first = browser.find_elements_by_css_selector('.product-grid')[0]
    product_first.location_once_scrolled_into_view
    compare_button = product_first.find_element_by_css_selector('[data-original-title ="Add to Wish List"]')
    compare_button.click()
    wish_list = browser.find_element_by_css_selector(browser.find_element_by_css_selector(
        'body nav div div:nth-child(2) ul li:nth-child(3) a').title)
    assert wish_list ==  "Wish List (1)"


# 5. Проверка добавления товаров в сравнение Compare
@pytest.mark.parametrize("product_index", [1, 5, 11])
def test_add_to_compare(browser, url, product_index, wait):
    catalog_page_url = url + f'/index.php?route=product/category&path=20'
    browser.get(catalog_page_url)
    product_first = browser.find_elements_by_css_selector('.product-grid')[0]
    product_first.location_once_scrolled_into_view
    compare_button = product_first.find_element_by_css_selector('[data-original-title="Compare this Product"]')
    compare_button.click()
    product_second = browser.find_elements_by_css_selector('.product-grid')[product_index]
    product_second.location_once_scrolled_into_view
    second_product_name_js = str(
        f'return document.querySelectorAll(".product-layout .img-responsive")[' + str(product_index) + f'].title;')
    second_product_name = browser.execute_script(second_product_name_js)
    second_compare = product_second.find_element_by_css_selector('[data-original-title="Compare this Product"]')
    second_compare.click()
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#compare-total')))
    button.click()
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#content tbody tr strong')))
    second_compare_product = browser.find_elements_by_css_selector('#content tbody tr strong')[1].text
    assert second_compare_product == str(second_product_name)