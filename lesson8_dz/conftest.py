import pytest
from selenium import webdriver
from webdrivermanager import GeckoDriverManager
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import ChromeOptions
from webdrivermanager import ChromeDriverManager



def test_addoption(parser):
    parser.addoption('--browser', '-B', action="store", default='firefox', required=False,
                     choices=['firefox','chrome'], help='browser')
    parser.addoption("--url", "-U", action="store", default="http://localhost/")


@pytest.fixture
def url(request):
    return request.config.getoption("--url")


@pytest.fixture
def browser(request):
    browser = request.config.getoption()
    if browser == 'Firefox':
        gdm = GeckoDriverManager()
        gdm.download_and_install()
        option = FirefoxOptions()
        # option.add_argument('--kiosk')
        option.headless = True
        wd = webdriver.Firefox(options=option)
        request.addfinalizer(wd.quit)
        return wd
    if browser == 'Chrome':
        cdm = ChromeDriverManager()
        cdm.download_and_install()
        option = ChromeOptions()
        # option.add_argument('--kiosk')
        # option.add_argument('--ignore-certificate-errors')
        option.headless = True
        wd = webdriver.Chrome(options=option)
        request.addfinalizer(wd.quit)
        return wd
    else:
        raise Exception(f'{request.param} is not supported!')
