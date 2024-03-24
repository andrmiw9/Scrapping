import time
from math import ceil
from sys import stdout

import requests
import loguru
from colorama import Back
from loguru import logger


def logger_set_up(level: str = 'TRACE') -> None:
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


def make_request(url: str) -> list:
    """ Make request """
    logger: loguru.Logger = loguru.logger.bind(object_id='Requester')
    try:
        logger.trace(f"Request: {url}")
        res = requests.get(url)
        logger.debug(f'Result: {res}')
        logger.debug(f'Content len: {len(res.text)} symbols')

        if res.text == 'false':
            raise requests.RequestException('Probably wrong request url')

        return list(res.json())

    except requests.RequestException as e:
        logger.error(f'Error: {e}')
    except TypeError as e:
        logger.exception(f'Error with response data. Most likely error with link or site. Error: {e}')


def main(base_url: str = 'https://htreviews.org/getData?o={0}&action=experts', load_count: int = 2) -> None:
    """ Main function """

    if load_count < 1:
        print(f'Nothing to parse, exiting...')
        return

    logger_set_up()
    _logger: loguru.Logger = loguru.logger.bind(object_id='Run main')
    _logger.info("Logger up")
    _logger.debug(f'Got {load_count} load_count')
    reviews_count = 20 if load_count < 20 else ceil(load_count / 20) * 20
    _logger.debug(f'Requests count interpretation: {reviews_count = }')

    data_list = []
    # TODO переделать, тут 20 нифига не нужно
    try:
        for i in range(0, reviews_count, 20):
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
    _base_url = 'https://htreviews.org/getData?o={0}&action=experts'
    _load_count = 11  # кол-во отзывов на загрузку и выдачу
    try:
        main(_base_url, _load_count)
    except KeyboardInterrupt:  # clearer output
        print(f'KeyboardInterrupt')
