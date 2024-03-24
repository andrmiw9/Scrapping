""" Test different webdrivers for selenium """


def chromium(test_url):
    """ Test that chromium webdriver is OK"""
    from selenium import webdriver
    # from selenium.webdriver.chrome import webdriver
    # from selenium.webdriver.chrome.service import service
    from selenium.webdriver.chrome.service import Service
    #

    options = webdriver.ChromeOptions()
    # options.add_argument(f"user-agent={persona['user-agent']}")
    options.add_argument('--headless')

    srvc = Service('./chrome-win64/chrome.exe')
    # srvc.path = './chrome-win64/chrome.exe'
    driver = webdriver.Chrome(service=srvc)
    driver.get(test_url)
    # driver.get_screenshot_as_file('./screenshot.png')
    # driver.get_elements_by_class_name('b239-a')
    driver.close()
    driver.quit()
    pass


if __name__ == '__main__':
    # test_url = 'https://www.ozon.ru'
    test_url = 'https://www.google.ru/'
    chromium(test_url)
