import os

from utils import JSONFile, Log

from lanka_data_timeseries.constants import DIR_TMP_DATA
from utils_future import Git

log = Log('combine_all')


def get_data_small(d: dict) -> dict:
    return dict(
        source_id=d['source_id'],
        category=d['category'],
        sub_category=d['sub_category'],
        scale=d['scale'],
        # unit=d['unit'],
        # footnotes=d['footnotes'],
        # frequency_name=d['frequency_name'],
        cleaned_data=d['cleaned_data'],
    )


def get_source_file_path_list() -> list[str]:
    file_path_list = []
    for dir_only in os.listdir(os.path.join(DIR_TMP_DATA, 'sources')):
        dir_source = os.path.join(DIR_TMP_DATA, 'sources', dir_only)
        if not os.path.isdir(dir_source):
            continue

        for file_only in os.listdir(dir_source):
            if 'summary.json' in file_only:
                continue
            file_path = os.path.join(dir_source, file_only)
            file_path_list.append(file_path)

    return file_path_list


def combine():
    file_path_list = get_source_file_path_list()
    data_list = []
    n = len(file_path_list)
    for i, file_path in enumerate(file_path_list):
        data = JSONFile(file_path).read()
        data_small = get_data_small(data)
        data_list.append(data_small)
        log.debug(f'{i + 1}/{n}) {file_path}')

    all_data_path = os.path.join(DIR_TMP_DATA, 'all.json')
    JSONFile(all_data_path).write(data_list)
    file_size = os.path.getsize(all_data_path) / 1_000_000
    log.info(
        f'Wrote {n} data tables to {all_data_path} ({file_size:.2f} MB))'
    )


def main():
    git = Git.from_github('nuuuwan', 'lanka_data_timeseries')
    git.clone(DIR_TMP_DATA, 'data')

    combine()


if __name__ == '__main__':
    main()
