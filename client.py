import logging
import os
import random
import sys
import time

from requests import get, RequestException


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    try:
        while True:
            try:
                client_id = random.randrange(1, 1000)
                logger.info(f'Attempting to send a request using {client_id} client_id')
                r = get(url=f'http://localhost:80/?clientId={client_id}')
                logger.info(r.status_code)
            except RequestException as e:
                logger.error(e)

            sleep_time = random.uniform(0.01, 0.02)
            print(f'Taking {sleep_time} seconds to nap')
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print('Exiting the application')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)