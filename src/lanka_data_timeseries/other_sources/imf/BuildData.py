import os

from utils import JSONFile, Log

from lanka_data_timeseries.common import clean_str
from lanka_data_timeseries.common_statistics import get_summary_statistics
from lanka_data_timeseries.constants import (ALPHA3_LKA,
                                             DEFAULT_FREQUENCY_NAME,
                                             DEFAULT_I_SUBJECT, DEFAULT_SCALE,
                                             DIR_TMP_DATA)
from utils_future import WWWFuture

URL_API = 'https://www.imf.org/external/datamapper/api/v1'
URL_INDICATORS = URL_API + '/indicators'
SOURCE_ID = 'imf'
DEFAULT_CATEGORY = 'IMF - Sri Lanka Data'

log = Log(__name__)


def get_indicator_idx() -> list[str]:
    data = WWWFuture.get_json(URL_INDICATORS)
    return data['indicators']


def url_lka(indicator_key: str):
    return f'{URL_API}/{indicator_key}/{ALPHA3_LKA}'


def get_lka_data(indicator_key: str):
    url = url_lka(indicator_key)
    raw_data = WWWFuture.get_json(url)
    return (
        raw_data.get('values', {}).get(indicator_key, {}).get(ALPHA3_LKA, {})
    )


def build_indicator_d(indicator_key, metadata):
    data = get_lka_data(indicator_key)
    summary_statistics = get_summary_statistics(data)
    label = metadata['label']
    if not label or str(label) == 'null':
        log.warning(f'No data for {indicator_key}')

    return dict(
        source_id=SOURCE_ID,
        category=DEFAULT_CATEGORY,
        sub_category=clean_str(label),
        scale=DEFAULT_SCALE,
        unit=metadata['unit'],
        frequency_name=DEFAULT_FREQUENCY_NAME,
        i_subject=DEFAULT_I_SUBJECT,
        footnotes=dict(
            indicator_key=indicator_key,
            description=metadata['description'],
            source=metadata['source'],
            dataset=metadata['dataset'],
            url=url_lka(indicator_key),
        ),
        summary_statistics=summary_statistics,
        cleaned_data=data,
        raw_data=data,
    )


def build_indicator(i, indicator_key, metadata, dir_output, n_indicators):
    d = build_indicator_d(indicator_key, metadata)

    n = d['summary_statistics']['n']
    if n <= 0:
        log.warning(f'No data for {indicator_key}')
        return

    file_path = os.path.join(
        dir_output,
        f'{SOURCE_ID}.{d["sub_category"]}.{DEFAULT_FREQUENCY_NAME}.json',
    )
    JSONFile(file_path).write(d)
    log.debug(f'{i}/{n_indicators}) Wrote {file_path} ({n} values)')


def build_data():
    dir_output = os.path.join(
        DIR_TMP_DATA,
        'sources',
        SOURCE_ID,
    )
    if not os.path.exists(dir_output):
        os.makedirs(dir_output)
        log.debug(f'Created {dir_output}')

    indicator_idx = get_indicator_idx()
    n_indicators = len(indicator_idx)
    i = 0
    for indicator_key, metadata in indicator_idx.items():
        i += 1
        build_indicator(i, indicator_key, metadata, dir_output, n_indicators)
