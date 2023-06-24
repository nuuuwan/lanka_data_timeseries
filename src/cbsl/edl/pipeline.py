from cbsl.edl.Frequency import FREQUENCY_LIST
from cbsl.edl.PageSearchCriteria import PageSearchCriteria
from cbsl.edl.PageSearchResult import PageSearchResult
from cbsl.edl.PageSelectItems import PageSelectItems

N_SUBJECTS = 35


def main():
    for frequency in FREQUENCY_LIST:
        for i_subject in range(0, N_SUBJECTS):
            webpage = PageSearchCriteria(frequency, i_subject).run()
            webpage = PageSelectItems(webpage).run()
            webpage = PageSearchResult(webpage).run()
            webpage.close()


if __name__ == '__main__':
    main()
