import csv
import os
import tempfile
import zipfile

from utils import WWW, File, JSONFile, Log

from lanka_data_timeseries.cbsl import DataBuilder as CBSLDataBuilder
from lanka_data_timeseries.common import DIR_TMP_DATA, clean_str

SOURCE_ID = 'world_bank'

URL_DOWNLOAD = (
    'https://api.worldbank.org' + '/v2/en/country/LKA' + '?downloadformat=csv'
)


URL_GIT_REPO = 'https://github.com/nuuuwan/lanka_data_timeseries.git'

BRANCH_DATA = 'data'

DEFAULT_CATEGORY = 'World Bank - Sri Lanka Data'
DEFAULT_SCALE = ''
DEFAULT_UNIT = ''
DEFAULT_FREQUENCY_NAME = 'Annual'
DEFAULT_I_SUBJECT = 0
DEFAULT_FOOTNOTES = {}

SOURCE_ID = 'world_bank'


log = Log(__name__)


def download_source() -> str:
    zip_path = tempfile.NamedTemporaryFile(suffix='.zip').name
    WWW.download_binary(URL_DOWNLOAD, zip_path)
    log.debug(f'Downloaded {URL_DOWNLOAD} to {zip_path}')

    dir_path = tempfile.NamedTemporaryFile().name
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dir_path)
    log.debug(f'Extracted {zip_path} to {dir_path}')

    for file_only in os.listdir(dir_path):
        if file_only.endswith('.csv') and file_only.startswith('API_LKA'):
            csv_path = os.path.join(dir_path, file_only)
            log.debug(f'Found {csv_path}')
            return csv_path
    raise Exception(f'No CSV file found in {dir_path}')


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
        if len(tokens) < 4 + len(year_list):
            continue
        sub_category = clean_str(tokens[2])
        data = {}

        for year, value in zip(year_list, tokens[4:-1]):
            data[year] = value

        raw_data = data
        cleaned_data = CBSLDataBuilder.clean_data(raw_data)
        summary_statistics = CBSLDataBuilder.get_summary_statistics(
            cleaned_data
        )

        details = dict(
            source_id=SOURCE_ID,
            category=DEFAULT_CATEGORY,
            sub_category=sub_category,
            scale=DEFAULT_SCALE,
            unit=DEFAULT_UNIT,
            frequency_name=DEFAULT_FREQUENCY_NAME,
            i_subject=DEFAULT_I_SUBJECT,
            footnotes=DEFAULT_FOOTNOTES,
            summary_statistics=summary_statistics,
            cleaned_data=cleaned_data,
            raw_data=raw_data,
        )

        # write detailed data (per sub_category) to new path
        new_data_path = os.path.join(
            dir_output_new,
            f'{SOURCE_ID}.{sub_category}.{DEFAULT_FREQUENCY_NAME}.json',
        )
        JSONFile(new_data_path).write(details)
        n = summary_statistics['n']
        log.debug(f'Wrote {n} time items to {new_data_path}')


if __name__ == '__main__':
    print(download_source())
