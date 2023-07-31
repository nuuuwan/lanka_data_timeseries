import os

from utils import CSVFile, JSONFile, Log

from lanka_data_timeseries.cbsl import DataBuilder as CBSLDataBuilder
from lanka_data_timeseries.common_statistics import get_summary_statistics
from lanka_data_timeseries.constants import (DEFAULT_FOOTNOTES,
                                             DEFAULT_FREQUENCY_NAME,
                                             DEFAULT_I_SUBJECT, DEFAULT_SCALE,
                                             DEFAULT_UNIT, DIR_TMP_DATA)

log = Log(__file__)

dir_data = os.path.join(
    'src',
    'lanka_data_timeseries',
    'other_sources',
    'misc',
    'multi_data',
    'data',
)


def get_dataset_group_list() -> list[str]:
    dataset_group_list = []
    for file_only in os.listdir(dir_data):
        if not file_only.endswith('.csv'):
            continue
        dataset_group = file_only[:-4]
        dataset_group_list.append(dataset_group)
    return dataset_group_list


def build_sub_category(
    dataset_group: str, metadata: dict, sub_category_data: dict
):
    sub_category_suffix = list(sub_category_data.values())[0]
    raw_data = dict(list(sub_category_data.items())[1:])
    cleaned_data = CBSLDataBuilder.clean_data(raw_data)
    summary_statistics = get_summary_statistics(cleaned_data)

    source_id = metadata['source_id']
    sub_category = dataset_group + ' - ' + sub_category_suffix
    frequency_name = metadata.get('frequency_name', DEFAULT_FREQUENCY_NAME)
    d = dict(
        source_id=source_id,
        category=dataset_group,
        sub_category=sub_category,
        frequency_name=frequency_name,
        scale=DEFAULT_SCALE,
        unit=metadata.get('unit', DEFAULT_UNIT),
        i_subject=DEFAULT_I_SUBJECT,
        footnotes=DEFAULT_FOOTNOTES,
        summary_statistics=summary_statistics,
        raw_data=raw_data,
        cleaned_data=cleaned_data,
    )

    id = f'{source_id}.{sub_category}.{frequency_name}'

    dir_source = os.path.join(DIR_TMP_DATA, 'sources', source_id)
    if not os.path.exists(dir_source):
        os.makedirs(dir_source)
        log.debug(f'Created {dir_source}')
    dataset_path = os.path.join(dir_source, id + '.json')
    JSONFile(dataset_path).write(d)

    n = summary_statistics['n']
    log.debug(f'Wrote {n} time-items to {dataset_path}')


def build_dataset_group(dataset_group: str):
    data_path = os.path.join(dir_data, dataset_group + '.csv')
    group_data = CSVFile(data_path).read()

    metadata_path = os.path.join(dir_data, dataset_group + '.json')
    metadata = JSONFile(metadata_path).read()

    keys = list(group_data[0].keys())
    keys[0]
    t_list = keys[1:]

    n_sub_categories = len(group_data)
    n_times = len(t_list)
    log.debug(
        f'Processing {n_sub_categories} sub-categories for {n_times} times'
    )

    for sub_category_data in group_data:
        build_sub_category(dataset_group, metadata, sub_category_data)


def build_data():
    dataset_group_list = get_dataset_group_list()
    for dataset_group in dataset_group_list:
        build_dataset_group(dataset_group)
