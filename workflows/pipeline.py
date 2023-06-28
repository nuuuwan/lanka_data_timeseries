from utils import Log

from cbsl.edl import (Config, PageSearchCriteria, PageSearchResult,
                      PageSelectItems)

log = Log(__name__)
MAX_CONFIGS = 5


def main():
    config_list = Config.random_list()
    for config in config_list[:MAX_CONFIGS]:
        log.debug(f'🟡Running {config}...')
        try:
            webpage2 = PageSearchCriteria(config).run()
            webpage3 = PageSelectItems(webpage2).run()
            webpage3 = PageSearchResult(webpage3).run()
            webpage3.close()

            log.info(f'✅ {config}: SUCCEEDED.')

        except BaseException as e:
            log.error(f'🔴 {config}: FAILED: ' + str(e))


if __name__ == '__main__':
    main()
