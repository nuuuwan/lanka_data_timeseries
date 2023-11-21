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
    'single_data',
    'data',
)


def get_sub_category_list() -> list[str]:
    sub_category_list = []
    for file_only in os.listdir(dir_data):
        if not file_only.endswith('.csv'):
            continue
        sub_category = file_only[:-4]
        sub_category_list.append(sub_category)
    return sub_category_list


def build_sub_category_d(sub_category: str, metadata: dict):
    data_path = os.path.join(dir_data, sub_category + '.csv')
    sub_category_data = CSVFile(data_path).read()

    raw_data = dict([d['time'], d['value']] for d in sub_category_data)
    cleaned_data = CBSLDataBuilder.clean_data(raw_data)
    summary_statistics = get_summary_statistics(cleaned_data)

    source_id = metadata['source_id']
    frequency_name = metadata.get('frequency_name', DEFAULT_FREQUENCY_NAME)

    return dict(
        source_id=source_id,
        category=source_id.upper(),
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


def build_sub_category(sub_category: str):
    metadata_path = os.path.join(dir_data, sub_category + '.json')
    metadata = JSONFile(metadata_path).read()

    source_id = metadata['source_id']
    frequency_name = metadata.get('frequency_name', DEFAULT_FREQUENCY_NAME)

    d = build_sub_category_d(sub_category, metadata)

    id = f'{source_id}.{sub_category}.{frequency_name}'

    dir_source = os.path.join(DIR_TMP_DATA, 'sources', source_id)
    if not os.path.exists(dir_source):
        os.makedirs(dir_source)
        log.debug(f'Created {dir_source}')
    dataset_path = os.path.join(dir_source, id + '.json')
    JSONFile(dataset_path).write(d)

    n = d['summary_statistics']['n']
    log.debug(f'Wrote {n} time-items to {dataset_path}')


def build_data():
    sub_category_list = get_sub_category_list()
    for sub_category in sub_category_list:
        build_sub_category(sub_category)
