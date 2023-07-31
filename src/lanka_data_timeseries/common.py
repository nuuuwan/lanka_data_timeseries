import re

from lanka_data_timeseries.constants import HALVES, MONTHS, QUARTERS

DEFAULT_SCALE = ''
DEFAULT_FREQUENCY_NAME = 'Annual'
DEFAULT_I_SUBJECT = -1
DEFAULT_UNIT = ''
DEFAULT_FOOTNOTES = {}


def clean_str(x):
    if x is None:
        return x
    x = x.replace('"', '')
    x = x.replace('%', 'Pct.')
    x = x.replace('/', ' or ')
    x = x.replace(':', '_')
    x = x.replace(';', '_')
    x = x.replace('+', '_')
    x = x.replace('\n', ' ')
    x = x.replace(',', ' ')
    x = x.replace('|', '_')
    x = re.sub(r'\s+', ' ', x).strip()
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


def normalize_time(t: str) -> str:
    if len(t) == 4:
        t = f'{t}-01-01'

    if len(t) == 7:
        t = f'{t}-01'

    return t


def clean_time(t: str) -> str:
    t = t.replace('"', '')

    if len(t) == 7 and t[4] == '/':
        t = t[:4] + '-07-01'

    for i, month in enumerate(MONTHS):
        t = t.replace(month, f'{i+1:02d}')

    for i, quarter in enumerate(QUARTERS):
        m = (i + 1) * 3
        t = t.replace(quarter, f'{m:02d}')

    for i, half in enumerate(HALVES):
        m = (i + 1) * 6
        t = t.replace(half, f'{m:02d}')

    return normalize_time(t)


def clean_value(x: str):
    if x == '-':
        return 0

    x = x.replace('"', '')
    x = x.replace(' ', '')

    if x.startswith('(') and x.endswith(')'):
        x = '-' + x[1:-1]

    if x.lower() in ['...', '', 'n.a', 'n.a.']:
        return None

    x = x.replace(',', '')
    x = x.replace('l', '1')
    x = x.replace('I', '1')
    x = x.replace("'", '')

    return parse_number(x)
