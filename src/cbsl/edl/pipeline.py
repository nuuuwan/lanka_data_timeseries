from cbsl.edl.Frequency import FREQUENCY_LIST
from cbsl.edl.PageSearchCriteria import PageSearchCriteria
from cbsl.edl.PageSearchResult import PageSearchResult
from cbsl.edl.PageSelectItems import PageSelectItems


def main():
    N_SUBJECT = 35
    for frequency in FREQUENCY_LIST:
        for i_subject in range(0, N_SUBJECT):
            webpage = PageSearchCriteria(frequency, i_subject).run()
            webpage = PageSelectItems(webpage).run()
            webpage = PageSearchResult(webpage).run()
            webpage.close()


if __name__ == '__main__':
    main()
