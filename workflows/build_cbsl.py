import os

from utils import Log

from lanka_data_timeseries.cbsl import (Config, PageSearchCriteria,
                                        PageSearchResult, PageSelectItems)
from lanka_data_timeseries.constants import DIR_TMP_DATA

log = Log(__name__)
MAX_CONFIGS = 10


def inner_unsafe(config):
    log.debug(f'🟡Running {config}...')
    webpage2 = PageSearchCriteria(config).run()
    webpage3 = PageSelectItems(webpage2).run()
    webpage3 = PageSearchResult(webpage3, config).run()
    webpage3.close()

    log.info(f'✅ {config}: SUCCEEDED.')
    return True


def inner(config):
    try:
        return inner_unsafe(config)

    except BaseException as e:
        log.error(f'🔴 {config}: FAILED: ' + str(e))
        return False


def init():
    os.makedirs(DIR_TMP_DATA)
    log.debug(f'Created {DIR_TMP_DATA}.')


def main():
    init()
    config_list = Config.random_list()
    n = 0
    n_success = 0
    for config in config_list[:MAX_CONFIGS]:
        success = inner(config)
        n += 1
        if success:
            n_success += 1

    message = '✅' * n_success + '🔴' * (n - n_success)
    if n_success == n:
        log.info(message)
    elif n_success == 0:
        log.error(message)
    else:
        log.warning(message)


if __name__ == '__main__':
    main()
