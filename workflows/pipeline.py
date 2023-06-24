from utils import Log

from cbsl.edl import (Config, PageSearchCriteria, PageSearchResult,
                      PageSelectItems)

log = Log(__name__)
MAX_N_SUCCESS = 5


def main():
    n_success = 0
    for config in Config.random_list():
        try:
            webpage2 = PageSearchCriteria(config).run()
            webpage3 = PageSelectItems(webpage2).run()
            webpage3 = PageSearchResult(webpage3).run()
            webpage3.close()
            log.info(f'✅ Completed {config}.')
            n_success += 1
            if n_success >= MAX_N_SUCCESS:
                break

        except BaseException:
            log.error(f'🔴 Failed to complete {config}.')
            continue


if __name__ == '__main__':
    main()
