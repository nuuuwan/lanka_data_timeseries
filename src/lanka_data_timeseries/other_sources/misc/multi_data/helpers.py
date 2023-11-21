import os

from utils import JSONFile, Log

from lanka_data_timeseries.cbsl import DataBuilder as CBSLDataBuilder
from lanka_data_timeseries.common_statistics import get_summary_statistics
from lanka_data_timeseries.constants import (DEFAULT_FOOTNOTES,
                                             DEFAULT_FREQUENCY_NAME,
                                             DEFAULT_I_SUBJECT, DEFAULT_SCALE,
                                             DEFAULT_UNIT, DIR_TMP_DATA)

log = Log(__file__)


def build_sub_category_d(
    sub_category_data: dict,
    metadata: dict,
    dataset_group: str,
    sub_category_suffix: str,
    frequency_name: str,
):
    raw_data = dict(list(sub_category_data.items())[1:])
    cleaned_data = CBSLDataBuilder.clean_data(raw_data)
    summary_statistics = get_summary_statistics(cleaned_data)

    source_id = metadata['source_id']
    sub_category = dataset_group + ' - ' + sub_category_suffix

    return dict(
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


def build_sub_category(
    dataset_group: str, metadata: dict, sub_category_data: dict
):
    sub_category_suffix = list(sub_category_data.values())[0]
    source_id = metadata['source_id']
    sub_category = dataset_group + ' - ' + sub_category_suffix
    frequency_name = metadata.get('frequency_name', DEFAULT_FREQUENCY_NAME)

    d = build_sub_category_d(
        sub_category_data,
        metadata,
        dataset_group,
        sub_category_suffix,
        frequency_name,
    )

    id = f'{source_id}.{sub_category}.{frequency_name}'

    dir_source = os.path.join(DIR_TMP_DATA, 'sources', source_id)
    if not os.path.exists(dir_source):
        os.makedirs(dir_source)
        log.debug(f'Created {dir_source}')
    dataset_path = os.path.join(dir_source, id + '.json')
    JSONFile(dataset_path).write(d)

    n = d['summary_statistics']['n']
    log.debug(f'Wrote {n} time-items to {dataset_path}')
