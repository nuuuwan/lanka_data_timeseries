import os

from utils import TIME_FORMAT_TIME, Git, JSONFile, Log

from src.lanka_data_timeseries.constants import DIR_TMP_DATA
from src.lanka_data_timeseries.summary.content_builders import (
    build_combined_summary, build_readme)
from utils_future import GitFuture

log = Log(__name__)
URL_GIT_REPO = 'https://github.com/nuuuwan/lanka_data_timeseries.git'
BRANCH_DATA = 'data'


def init():
    git = Git(URL_GIT_REPO)
    git.clone(DIR_TMP_DATA, force=False)
    git.checkout(BRANCH_DATA)


def get_source_id_list():
    dir_sources = os.path.join(DIR_TMP_DATA, 'sources')
    source_id_list = []
    for file_name_only in os.listdir(dir_sources):
        if os.path.isdir(os.path.join(dir_sources, file_name_only)):
            source_id_list.append(file_name_only)
    return source_id_list


def get_data_list(source_id):
    git_future = GitFuture(DIR_TMP_DATA)
    dir_data = os.path.join(DIR_TMP_DATA, 'sources', source_id)
    d_list = []
    for file_name_only in os.listdir(dir_data):
        if not file_name_only.endswith('.json'):
            continue
        if file_name_only in [
            'summary.json',
            '--log-success-summary.json',
        ]:
            continue
        file_path = os.path.join(dir_data, file_name_only)
        d = JSONFile(file_path).read()
        assert d['source_id'] == source_id

        last_updated_time = git_future.get_last_update_ut(file_path)
        d['last_updated_time_ut'] = last_updated_time.ut
        d['last_updated_time_str'] = TIME_FORMAT_TIME.stringify(
            last_updated_time
        )
        d_list.append(d)

    d_list = sorted(
        d_list, key=lambda x: x['sub_category'] + x['frequency_name']
    )
    len(d_list)
    return d_list


def extract(d):
    del d['raw_data']
    del d['cleaned_data']
    return d


def write(data_list_all, source_id):
    summary_data_list = [extract(d) for d in data_list_all]
    file_path = os.path.join(
        DIR_TMP_DATA, 'sources', source_id, 'summary.json'
    )
    JSONFile(file_path).write(summary_data_list)
    file_size = os.path.getsize(file_path) / 1_000_000
    log.debug(
        f'Wrote {len(summary_data_list)} data items'
        + f' to "{file_path}" ({file_size:.2f}MB)'
    )
    return summary_data_list


def build_individual_summaries():
    source_id_list = get_source_id_list()
    combined_summary_data_list = []
    for source_id in source_id_list:
        data_list = get_data_list(source_id)
        summary_data_list = write(data_list, source_id)
        combined_summary_data_list += summary_data_list
    return combined_summary_data_list


def build():
    init()
    combined_summary_data_list = build_individual_summaries()
    build_combined_summary(combined_summary_data_list)
    build_readme(combined_summary_data_list)
