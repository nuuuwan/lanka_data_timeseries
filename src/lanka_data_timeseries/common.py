import re


def clean_str(x):
    if x is None:
        return x
    x = x.replace('"', '')
    x = x.replace('%', 'Pct.')
    x = x.replace('/', ' or ')
    x = x.replace(':', '_')
    x = x.replace('+', '_')
    x = x.replace('\n', ' ')
    x = x.replace(',', ' ')
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
