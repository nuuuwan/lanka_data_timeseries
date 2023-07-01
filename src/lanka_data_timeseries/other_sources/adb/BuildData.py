import os
import tempfile

from openpyxl import load_workbook
from utils import JSONFile, Log

from lanka_data_timeseries.cbsl import DataBuilder as CBSLDataBuilder
from lanka_data_timeseries.common import (DEFAULT_FOOTNOTES,
                                          DEFAULT_FREQUENCY_NAME,
                                          DEFAULT_I_SUBJECT, DEFAULT_SCALE,
                                          DEFAULT_UNIT, clean_str,
                                          parse_number)

log = Log(__file__)


SOURCE_ID = 'adb'
I_COL_CATEGORY = 2
I_ROW_T_HEADER = 7
EXCEL_PATH = os.path.join(
    'src',
    'lanka_data_timeseries',
    'other_sources',
    'adb',
    'sri-key-indicators-2022.xlsx',
)

INDENT_STR = ' ' * 5


def init_dir():
    dir_output = os.path.join(
        tempfile.gettempdir(),
        'tmp.lanka_data_timeseries',
        'sources',
        SOURCE_ID,
    )
    if not os.path.exists(dir_output):
        os.makedirs(dir_output)
        log.debug(f'Created {dir_output}')
    return dir_output


def parse_excel():
    workbook = load_workbook(EXCEL_PATH)
    worksheet = workbook.active

    i_col = 3
    year_list = []
    while True:
        year_str = worksheet.cell(row=I_ROW_T_HEADER, column=i_col).value
        i_col += 1

        if not year_str:
            break
        year = int(year_str)
        year_list.append(year)

    i_row = I_ROW_T_HEADER + 1
    indent_to_text = ['' for _ in range(5)]
    category1 = ''
    last_unit = ''
    d_list = []
    while True:
        if i_row > 1_000:
            break

        category_str = worksheet.cell(row=i_row, column=I_COL_CATEGORY).value

        data = {}
        for i_year, year in enumerate(year_list):
            value = worksheet.cell(row=i_row, column=3 + i_year).value
            data[year] = parse_number(str(value))

        data = dict([item for item in data.items() if item[1] is not None])

        # data reading complete
        i_row += 1

        if not category_str:
            continue

        if '(' in category_str:
            last_unit = category_str.split('(')[1].split(')')[0]

        first_word = category_str.split(' ')[0]
        if first_word.isupper() and first_word not in ['GDP', 'GNI']:
            category1 = category_str.strip()
            continue

        n_leading_spaces = len(category_str) - len(category_str.lstrip())
        if n_leading_spaces % 5 != 0:
            raise Exception(
                f'Unexpected indent ({n_leading_spaces}): {category_str}'
            )
        i = n_leading_spaces // 5
        indent_to_text[i] = category_str.strip()

        category = category1
        sub_category = ' - '.join(indent_to_text[: i + 1])

        summary_statistics = CBSLDataBuilder.get_summary_statistics(data)

        if last_unit in category_str or last_unit in sub_category:
            unit = last_unit
        else:
            unit = DEFAULT_UNIT

        n_non_none = sum(1 for v in data.values() if v is not None)
        if n_non_none == 0:
            continue

        d = dict(
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
        d_list.append(d)
        print(d['category'])
        print(d['sub_category'])
        print(list(d['cleaned_data'].items())[0])
        print('-' * 32)
    return d_list


def build_details(d_list, dir_output):
    file_path_set = set()
    for d in d_list:
        sub_category = d['sub_category']
        file_path = os.path.join(
            dir_output,
            f'{SOURCE_ID}.{sub_category}.{DEFAULT_FREQUENCY_NAME}.json',
        )
        if file_path in file_path_set:
            log.error(f'Duplicate file path: {file_path}')
        file_path_set.add(file_path)
        JSONFile(file_path).write(d)
        # log.debug(f'Wrote {file_path}')


def build_summary(d_list, dir_output):
    summary_d_list = []
    for d in d_list:
        summary_d = d
        del summary_d['cleaned_data']
        del summary_d['raw_data']
        summary_d_list.append(summary_d)

    file_path = os.path.join(
        dir_output,
        'summary.json',
    )
    JSONFile(file_path).write(summary_d_list)
    log.debug(f'Wrote {file_path}')


def build_data():
    dir_output = init_dir()
    d_list = parse_excel()
    build_details(d_list, dir_output)
    build_summary(d_list, dir_output)
