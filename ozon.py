"""
Парсим OZON видюхи, 4070 и 4080 (все версии)
Сортировка по рейтингу
"""
import time
from sys import stdout

import loguru
import selenium
import requests
from colorama import Back
from loguru import logger
from selenium.webdriver.chromium import webdriver


def logger_set_up(level: str = 'TRACE', make_log_file: bool = False) -> None:
    """Loguru set up"""
    logger.remove()  # this removes duplicates in the console if we use the custom log format
    logger.configure(extra={"object_id": "None"})  # Default values if not bind extra variable
    logger.level("HL", no=38, color=Back.MAGENTA, icon="🔺")
    logger.level(f"TRACE", color="<fg #1b7c80>")  # выставить цвет
    logger.level(f"SUCCESS", color="<bold><fg #2dd644>")  # выставить цвет

    # формат и цвета логов
    log_format: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>[<level>{level}</level>]" \
                      "<cyan>[{extra[object_id]}]</cyan>" \
                      "<magenta>{function}</magenta>:" \
                      "<cyan>{line}</cyan> - <level>{message}</level>"

    logger.add(sink=stdout,
               format=log_format,
               colorize=True,
               enqueue=True,  # for better work of async
               level=level)  # mb backtrace=True?

    if make_log_file:
        logger.add(sink="ozon.log",
                   format=log_format,
                   colorize=True,
                   enqueue=True,  # for better work of async
                   level=level)


def make_request(url: str) -> list:
    """ Make request """
    logger: loguru.Logger = loguru.logger.bind(object_id='Requester')
    try:
        logger.trace(f"Request url: {url}")
        # res = requests.get(url)

        driver.get(url)

        # Получаем заголовки товаров
        titles = driver.find_elements_by_css_selector(".b5v1")

        for title in titles:
            print(title.text)

        driver.quit()
        logger.debug(f'Result: {res}')
        logger.debug(f'Content len: {len(res.text)} symbols')
        if res.status_code != 200:
            raise requests.RequestException(f'Request failed with status code: {res.status_code}')

        if res.text == 'false':
            raise requests.RequestException('Probably wrong request url')

        return list(res.json())

    except requests.RequestException as e:
        logger.error(f'Error: {e}')
    except TypeError as e:
        logger.exception(f'Error with response data. Most likely error with link or site. Error: {e}')


def setup_webdriver() -> webdriver:
    driver = webdriver.Chrome(executable_path='путь_к_драйверу')
    return driver


def main(base_url: str, page_count: int = 2) -> None:
    """ Main function """

    if page_count < 1:
        print(f'Nothing to parse, exiting...')
        return

    logger_set_up()
    _logger: loguru.Logger = loguru.logger.bind(object_id='Run main')
    _logger.info("Logger up")
    _logger.debug(f'Got {page_count = }')

    data_list = []
    try:
        for i in range(page_count):
            logger.trace("\n")
            _url = base_url.format(i)

            res_data = make_request(_url)
            if res_data:
                data_list.extend(res_data)
                logger.trace(f'Result: {res_data}')
            else:
                logger.warning(f'Request data result is None or empty')

            time.sleep(0.5)  # sleep for 0.5 sec for not getting banned from htreviews

    except requests.RequestException as e:
        logger.error(f'Error: {e}')

    pass


if __name__ == '__main__':
    # видюхи на озоне, 4070 и 4080 (все версии)
    _base_url = 'https://www.ozon.ru/category/videokarty-15721/?gpuseries=100429744%2C100465304%2C100482563'
    '%2C100482562%2C101092656%2C101092661%2C101092657%2C100482560&opened=gpuseries&page={0}&sorting=rating'
    _page_count = 3  # кол-во страниц предложений распарсить
    try:
        main(_base_url)
    except KeyboardInterrupt:  # clearer output
        print(f'KeyboardInterrupt')
