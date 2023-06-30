from lanka_data_timeseries.cbsl import (BuildSuccessSummary, BuildSummary,
                                        EDLSummary)


def main():
    EDLSummary.build()
    BuildSummary.build()
    BuildSuccessSummary.build()


if __name__ == '__main__':
    main()
