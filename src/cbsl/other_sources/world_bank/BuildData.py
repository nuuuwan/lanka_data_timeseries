import csv
import os
import tempfile

from utils import File, JSONFile, Log,Git

CSV_PATH = os.path.join(
    'src',
    'cbsl',
    'other_sources',
    'world_bank',
    'API_LKA_DS2_en_csv_v2_5554850.csv',
)

URL_GIT_REPO = 'https://github.com/nuuuwan/cbsl.git'
DIR_TMP_DATA = os.path.join(tempfile.gettempdir(), 'tmp.cbsl')
BRANCH_DATA = 'data'

log = Log(__name__)


def clean_str(x):
    x = x.replace('"', '')
    x = x.replace('%', 'Pct.')
    x = x.replace('/', ' or ')
    x = x.replace(':', '_')
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
    dir_output = os.path.join(DIR_TMP_DATA, 'other_sources', 'world_bank')
    if not os.path.exists(dir_output):
        os.makedirs(dir_output)
        log.debug(f'Created {dir_output}')

    lines = File(CSV_PATH).read_lines()

    year_list = lines[4].split(',')[4:-1]

    DEFAULT_CATEGORY = 'World Bank - Sri Lanka Data'
    DEFAULT_SCALE = ''
    DEFAULT_UNIT = ''
    summary_data_list = []
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
            year = parse_int(year)
            value = parse_number(value)
            if value is None:
                continue
            data[year] = value
        details = dict(
            scale=DEFAULT_SCALE,
            unit=DEFAULT_UNIT,
            data=data,
        )

        ts = list(data.keys())
        if len(ts) == 0:
            continue
        min_t, max_t = min(ts), max(ts)
        latest_value = data[max_t]
        n = len(data)
        summary_data = dict(
            min_t=min_t,
            max_t=max_t,
            latest_value=latest_value,
            n=n,
            category=DEFAULT_CATEGORY,
            sub_category=sub_category,
            unit=DEFAULT_UNIT,
            scale=DEFAULT_SCALE,
        )
        summary_data_list.append(summary_data)

        data_path = os.path.join(
            dir_output, f'{DEFAULT_CATEGORY}.{sub_category}.json'
        )
        JSONFile(data_path).write(details)
        log.debug(f'Wrote {n} time items to {data_path}')

    summary_path = os.path.join(dir_output, 'summary.json')
    JSONFile(summary_path).write(summary_data_list)
    log.debug(f'Wrote {len(summary_data_list)} items to {summary_path}')


def main():
    git = Git(URL_GIT_REPO)
    git.clone(DIR_TMP_DATA, force=True)
    git.checkout(BRANCH_DATA)

    build_data()

    git.add_and_commit(DIR_TMP_DATA, 'Updated World Bank Data')
    git.push(BRANCH_DATA)


if __name__ == '__main__':
    main()
