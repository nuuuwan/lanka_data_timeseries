import os

from utils import CSVFile, JSONFile, Log

from lanka_data_timeseries.other_sources.misc.multi_data.helpers import \
    build_sub_category

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
