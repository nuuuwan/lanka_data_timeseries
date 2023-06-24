from cbsl.edl import EDLCategoryTables, EDLSummary


def main():
    EDLSummary.build()
    EDLCategoryTables.build()


if __name__ == '__main__':
    main()
