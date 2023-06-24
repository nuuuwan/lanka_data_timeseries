from utils import Log, get_time_id

from cbsl.edl import (FREQUENCY_LIST, N_SUBJECTS, PageSearchCriteria,
                      PageSearchResult, PageSelectItems)

log = Log(__name__)


def main():
    time_id = get_time_id()
    for frequency in FREQUENCY_LIST:
        for i_subject in range(0, N_SUBJECTS):
            try:
                webpage2 = PageSearchCriteria(frequency, i_subject).run()
                webpage3 = PageSelectItems(webpage2).run()
                webpage3 = PageSearchResult(webpage3).run(time_id)
                webpage3.close()
                log.info(f'✅ Completed {frequency}/{i_subject}.')

            except BaseException:
                log.error(f'🔴 Failed to complete {frequency}/{i_subject}.')
                continue


if __name__ == '__main__':
    main()
