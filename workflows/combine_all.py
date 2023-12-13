import os
from functools import cache

from utils import File, JSONFile, Log

from lanka_data_timeseries.constants import DIR_TMP_DATA
from utils_future import Git

log = Log('combine_all')


def get_data_compressed(d: dict) -> dict:
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


@cache
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


@cache
def get_data_list():
    file_path_list = get_source_file_path_list()
    return [JSONFile(file_path).read() for file_path in file_path_list]


def combine_as_json():
    original_data_list = get_data_list()
    data_list = [get_data_compressed(d) for d in original_data_list]
    all_data_path = os.path.join(DIR_TMP_DATA, 'all.json')
    JSONFile(all_data_path).write(data_list)
    file_size = os.path.getsize(all_data_path) / 1_000_000
    n = len(original_data_list)
    log.info(
        f'Wrote {n} data tables to {all_data_path} ({file_size:.2f} MB))'
    )


def combine_as_txt():
    original_data_list = get_data_list()
    lines = []
    for d in original_data_list:
        title = d['category'] + ' ' + d['sub_category']
        lines.append(title)
        for k, v in d['cleaned_data'].items():
            lines.append(str(k) + '\t' + str(v))
        lines.append('')
        lines.append('Source: ' + d['source_id'])
        lines.append('Frequency: ' + d['frequency_name'])

        if d['unit']:
            lines.append('Unit: ' + d['unit'])

        if d['scale']:
            lines.append('Scale: ' + d['scale'])

        if d['footnotes']:
            lines.append('Footnotes: ' + str(d['footnotes']))

        lines.append('-' * 32)
        lines.append('')
    all_data_path = os.path.join(DIR_TMP_DATA, 'all.txt')
    File(all_data_path).write_lines(lines)
    file_size = os.path.getsize(all_data_path) / 1_000_000
    n = len(original_data_list)
    log.info(
        f'Wrote {n} data tables to {all_data_path} ({file_size:.2f} MB))'
    )


def combine_as_md():
    original_data_list = get_data_list()
    lines = []
    for d in original_data_list:
        title = d['category'] + ' ' + d['sub_category']
        lines.append('# ' + title)
        lines.append('')
        for k, v in d['cleaned_data'].items():
            lines.append(f'* {k}: {v}')
        lines.append('')

    all_data_md_path = os.path.join(DIR_TMP_DATA, 'all.md')
    File(all_data_md_path).write_lines(lines)
    file_size = os.path.getsize(all_data_md_path) / 1_000_000
    n = len(original_data_list)
    log.info(
        f'Wrote {n} data tables to {all_data_md_path} ({file_size:.2f} MB))'
    )


def combine_as_small_json():
    original_data_list = get_data_list()

    idx = {}
    for d in original_data_list:
        title = d['category'] + ' ' + d['sub_category']
        idx_inner = d['cleaned_data']
        idx[title] = idx_inner

    all_small_data_path = os.path.join(DIR_TMP_DATA, 'all.small.json')
    JSONFile(all_small_data_path).write(idx)
    file_size = os.path.getsize(all_small_data_path) / 1_000_000
    n = len(original_data_list)
    log.info(
        f'Wrote {n} data tables to {all_small_data_path} ({file_size:.2f} MB))'
    )


def main():
    git = Git.from_github('nuuuwan', 'lanka_data_timeseries')
    git.clone(DIR_TMP_DATA, 'data')

    combine_as_json()
    combine_as_txt()
    combine_as_md()
    combine_as_small_json()


if __name__ == '__main__':
    main()
