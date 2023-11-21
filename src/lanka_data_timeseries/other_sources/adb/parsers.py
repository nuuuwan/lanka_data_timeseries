from utils import Log

from lanka_data_timeseries.common import clean_str, parse_number
from lanka_data_timeseries.common_statistics import get_summary_statistics
from lanka_data_timeseries.constants import (DEFAULT_FOOTNOTES,
                                             DEFAULT_FREQUENCY_NAME,
                                             DEFAULT_I_SUBJECT, DEFAULT_SCALE,
                                             DEFAULT_UNIT)

log = Log(__file__)
SOURCE_ID = 'adb'

I_ROW_T_HEADER = 7


def parse_category(worksheet, i_row):
    I_COL_CATEGORY = 2
    return worksheet.cell(row=i_row, column=I_COL_CATEGORY).value


def parse_data(worksheet, i_row, year_list):
    data = {}
    for i_year, year in enumerate(year_list):
        value = worksheet.cell(row=i_row, column=3 + i_year).value
        data[year] = parse_number(str(value))

    return dict([item for item in data.items() if item[1] is not None])


def build_d(category1, indent_to_text, last_unit, data, i_row, i):
    category = category1
    sub_category = ' - '.join(indent_to_text[: i + 1])

    summary_statistics = get_summary_statistics(data)

    if last_unit in category or last_unit in sub_category:
        unit = last_unit
    else:
        unit = DEFAULT_UNIT

    return dict(
        source_id=SOURCE_ID,
        category=clean_str(category),
        sub_category=clean_str(sub_category),
        scale=DEFAULT_SCALE,
        unit=unit,
        frequency_name=DEFAULT_FREQUENCY_NAME,
        i_subject=DEFAULT_I_SUBJECT,
        footnotes=DEFAULT_FOOTNOTES,
        summary_statistics=summary_statistics,
        cleaned_data=data,
        raw_data=data,
    )


def is_valid_row(category_str, data, n_leading_spaces):
    if not category_str:
        return False

    is_n_non_none_zero = sum(1 for v in data.values() if v is not None) == 0

    first_word = category_str.split(' ')[0]
    is_first_word_invalid = first_word.isupper() and first_word not in [
        'GDP',
        'GNI',
    ]

    is_leading_spaces_invalud = n_leading_spaces % 5 != 0

    return not (
        is_n_non_none_zero
        or is_first_word_invalid
        or is_leading_spaces_invalud
    )


def parse_row(
    worksheet, i_row, year_list, indent_to_text, category1, last_unit
):
    category_str = parse_category(worksheet, i_row)
    data = parse_data(worksheet, i_row, year_list)
    i_row += 1

    n_leading_spaces = None
    if category_str:
        if '(' in category_str:
            last_unit = category_str.split('(')[1].split(')')[0]
        n_leading_spaces = len(category_str) - len(category_str.lstrip())

    if not is_valid_row(category_str, data, n_leading_spaces):
        return None, i_row, indent_to_text, category1, last_unit

    i = n_leading_spaces // 5
    indent_to_text[i] = category_str.strip()

    d = build_d(category1, indent_to_text, last_unit, data, i_row, i)
    return d, i_row, indent_to_text, category1, last_unit
