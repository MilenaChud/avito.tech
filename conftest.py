import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")


def pytest_addoption(parser):
    parser.addoption(
        "--browser", default="chrome", help="The browser for tests"
    )
    parser.addoption("--url", action="store", default="https://www.avito.ru/ekaterinburg/odezhda_obuv_aksessuary/plate_hm_2999116301", help="reference on the web-site"
                     )
    parser.addoption("--drivers", action="store_true", default=os.path.expanduser("~/Desktop/Drivers"),
                     help="path to drivers")


@pytest.fixture
def run_browser(request):
    browser = request.config.getoption("--browser")
    drivers_folder = request.config.getoption("--drivers")
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        service = ChromeService(executable_path=f"{drivers_folder}/chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)
    else:
        raise ValueError("This browser doesn't exists")

    yield driver
    driver.close()

