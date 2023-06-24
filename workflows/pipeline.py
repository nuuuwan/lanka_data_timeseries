from utils import Log, get_time_id

from cbsl.edl import (FREQUENCY_LIST, N_SUBJECTS, PageSearchCriteria,
                      PageSearchResult, PageSelectItems)

log = Log(__name__)


def main():
    time_id = get_time_id()
    for frequency in FREQUENCY_LIST:
        for i_subject in range(0, N_SUBJECTS):
            webpage = PageSearchCriteria(frequency, i_subject).run()

            try:
                webpage = PageSelectItems(webpage).run()
            except BaseException:
                log.error(f'🔴 Failed to complete {frequency}/{i_subject}.')
                continue

            webpage = PageSearchResult(webpage).run(time_id)

            webpage.close()

            log.info(f'✅ Completed {frequency}/{i_subject}.')


if __name__ == '__main__':
    main()
