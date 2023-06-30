import csv
import os
import tempfile

from utils import File, JSONFile, Log

from lanka_data_timeseries.cbsl import DataBuilder as CBSLDataBuilder

SOURCE_ID = 'world_bank'

CSV_PATH = os.path.join(
    'src',
    'lanka_data_timeseries',
    'other_sources',
    'world_bank',
    'API_LKA_DS2_en_csv_v2_5554850.csv',
)

URL_GIT_REPO = 'https://github.com/nuuuwan/lanka_data_timeseries.git'
DIR_TMP_DATA = os.path.join(
    tempfile.gettempdir(), 'tmp.lanka_data_timeseries'
)
BRANCH_DATA = 'data'

DEFAULT_CATEGORY = 'World Bank - Sri Lanka Data'
DEFAULT_SCALE = ''
DEFAULT_UNIT = ''
DEFAULT_FREQUENCY_NAME = 'Annual'
DEFAULT_I_SUBJECT = 0
DEFAULT_FOOTNOTES = {}

SOURCE_ID = 'world_bank'


log = Log(__name__)


def clean_str(x):
    x = x.replace('"', '')
    x = x.replace('%', 'Pct.')
    x = x.replace('/', ' or ')
    x = x.replace(':', '_')
    x = x.replace('+', '_')
    return x


def parse_int(x):
    x = clean_str(x)
    try:
        return int(x)
    except ValueError:
        return None


def parse_float(x):
    x = clean_str(x)
    try:
        return float(x)
    except ValueError:
        return None


def parse_number(x):
    i = parse_int(x)
    if i is not None:
        return i
    return parse_float(x)


def build_data():
    dir_output_new = os.path.join(DIR_TMP_DATA, 'sources', 'world_bank')
    if not os.path.exists(dir_output_new):
        os.makedirs(dir_output_new)
        log.debug(f'Created {dir_output_new}')

    lines = File(CSV_PATH).read_lines()

    year_list = lines[4].split(',')[4:-1]

    new_summary_data_list = []
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

        # new summary
        new_summary_data = dict(
            source_id=details['source_id'],
            category=details['category'],
            sub_category=details['sub_category'],
            frequency_name=details['frequency_name'],
            unit=details['unit'],
            scale=details['scale'],
            summary_statistics=details['summary_statistics'],
            footnotes={
                'source_file': 'API_LKA_DS2_en_csv_v2_5554850.csv',
            },
        )
        new_summary_data_list.append(new_summary_data)

    # write summary
    new_summary_path = os.path.join(dir_output_new, 'summary.json')
    JSONFile(new_summary_path).write(new_summary_data_list)
    log.debug(
        f'Wrote {len(new_summary_data_list)} items to {new_summary_path}'
    )
