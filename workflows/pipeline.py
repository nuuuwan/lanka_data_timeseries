from cbsl.edl import (FREQUENCY_LIST, N_SUBJECTS, PageSearchCriteria,
                      PageSearchResult, PageSelectItems)


def main():
    for frequency in FREQUENCY_LIST:
        for i_subject in range(0, N_SUBJECTS):
            webpage = PageSearchCriteria(frequency, i_subject).run()
            webpage = PageSelectItems(webpage).run()
            webpage = PageSearchResult(webpage).run()
            webpage.close()


if __name__ == '__main__':
    main()
