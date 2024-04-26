"""
WDADWA
"""

from sys import stdout

import loguru
import matplotlib.pyplot as plt
import pandas as pd
import requests
from colorama import Back
from loguru import logger


def set_up_plt(df_test2: pd.DataFrame) -> None:
    """

    :param df_test2:
    """
    logger: loguru.logger = loguru.logger.bind(object_id='SETUP_PLOT')
    logger.info(f'Setting up plot...')
    plt.subplot(2, 2, 1)
    plt.plot(df_test2['Position'], df_test2['Rating'])
    plt.xlabel('Position')
    plt.ylabel('Rating')
    plt.subplot(2, 2, 2)
    plt.plot(df_test2['Position'], df_test2['Stats'])
    plt.xlabel('Position')
    plt.ylabel('Stats')
    plt.subplot(2, 2, 3)
    plt.plot(df_test2['Position'], df_test2['Reviews'])
    plt.xlabel('Position')
    plt.ylabel('Reviews')
    plt.show()
    logger.debug(f'Ended setting up plot...')


def main(save_to_excel: bool = True) -> None:
    """ Main function """
    logger: loguru.logger = loguru.logger.bind(object_id='MAIN')
    position = []
    rating = []
    stats = []
    reviews = []

    i = 0
    upper_bound = 10000000
    while upper_bound:
        logger.debug(f'Iteration number: {i}')
        offset = 20

        _url = f'https://htreviews.org/getData?o={i * offset}&action=experts'
        logger.debug(f'URL: {_url}')
        response = requests.get(_url)

        if response.status_code != 200:
            logger.warning(f'Response status code: {response.status_code}')
            break

        jsoned = response.json()

        for k in jsoned:  # 20 users
            logger.trace(f'{k}')
            position.append(int(k["position"]))
            rating.append(int(k["rating"]))
            stats.append(int(k["ratings_count"]))
            reviews.append(int(k["reviews"]))

        #
        if len(jsoned) < 20:
            logger.info(f'Breaking...')
            break

        i += 1
        if i > 5:
            logger.warning(f'Кароче вырубаюсь потому что ты гавно. Иди нахуй!')
            break

    df_result: pd.DataFrame = pd.DataFrame({
        "Position": position,
        "Rating"  : rating,
        "Stats"   : stats,
        "Reviews" : reviews
    })

    # try:
    # raise IOError('EROROR MOTHERFUCKER!')
    # except IOError as e:
    #     logger.exception(f'Error: {e}')

    if save_to_excel:
        logger.info(f'Saving to excel...')
        df_result.to_excel('klim.xlsx', index=False)
    else:
        logger.warning(f'Skipping saving to excel...')

    set_up_plt(df_result)
    logger.debug(f'End of main function')


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


if __name__ == '__main__':
    logger_set_up()
    # logger: loguru.logger = loguru.logger.bind(object_id='Run main')
    logger.info(f'Running main...')
    main()
