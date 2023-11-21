import csv
import os
import tempfile

from utils import WWW, File, JSONFile, Log

from lanka_data_timeseries.cbsl import DataBuilder as CBSLDataBuilder
from lanka_data_timeseries.common import clean_str
from lanka_data_timeseries.common_statistics import get_summary_statistics
from lanka_data_timeseries.constants import (DEFAULT_FOOTNOTES,
                                             DEFAULT_FREQUENCY_NAME,
                                             DEFAULT_I_SUBJECT, DEFAULT_SCALE,
                                             DEFAULT_UNIT, DIR_TMP_DATA)
from utils_future import WWWFuture, ZipFile

SOURCE_ID = 'world_bank'
URL_DOWNLOAD = WWWFuture.join(
    'https://api.worldbank.org', 'v2/en/country', 'LKA?downloadformat=csv'
)
DEFAULT_CATEGORY = 'World Bank - Sri Lanka Data'


log = Log(__name__)


def download_source() -> str:
    zip_path = tempfile.NamedTemporaryFile(suffix='.zip').name
    WWW.download_binary(URL_DOWNLOAD, zip_path)

    dir_path = tempfile.NamedTemporaryFile().name
    ZipFile(zip_path).extractall(dir_path)

    for file_only in os.listdir(dir_path):
        if file_only.endswith('.csv') and file_only.startswith('API_LKA'):
            csv_path = os.path.join(dir_path, file_only)
            log.debug(f'Found {csv_path}')
            return csv_path
    raise Exception(f'No CSV file found in {dir_path}')


def build_data_row_d(
    tokens: list[str], year_list: list[str], sub_category
) -> dict:
    data = {}
    for year, value in zip(year_list, tokens[4:-1]):
        data[year] = value

    cleaned_data = CBSLDataBuilder.clean_data(data)

    return dict(
        source_id=SOURCE_ID,
        category=DEFAULT_CATEGORY,
        sub_category=sub_category,
        scale=DEFAULT_SCALE,
        unit=DEFAULT_UNIT,
        frequency_name=DEFAULT_FREQUENCY_NAME,
        i_subject=DEFAULT_I_SUBJECT,
        footnotes=DEFAULT_FOOTNOTES,
        summary_statistics=get_summary_statistics(cleaned_data),
        cleaned_data=cleaned_data,
        raw_data=data,
    )


def build_data_row(
    tokens: list[str], year_list: list[str], dir_output_new: str
):
    if len(tokens) < 4 + len(year_list):
        return
    sub_category = clean_str(tokens[2])
    d = build_data_row_d(tokens, year_list, sub_category)

    new_data_path = os.path.join(
        dir_output_new,
        f'{SOURCE_ID}.{sub_category}.{DEFAULT_FREQUENCY_NAME}.json',
    )
    JSONFile(new_data_path).write(d)
    n = d['summary_statistics']['n']
    log.debug(f'Wrote {n} time items to {new_data_path}')


def build_data():
    csv_path = download_source()
    dir_output_new = os.path.join(DIR_TMP_DATA, 'sources', 'world_bank')
    if not os.path.exists(dir_output_new):
        os.makedirs(dir_output_new)
        log.debug(f'Created {dir_output_new}')

    lines = File(csv_path).read_lines()
    year_list = lines[4].split(',')[4:-1]

    for tokens in csv.reader(
        lines[5:],
        quotechar='"',
        delimiter=',',
        quoting=csv.QUOTE_ALL,
        skipinitialspace=True,
    ):
        build_data_row(tokens, year_list, dir_output_new)
