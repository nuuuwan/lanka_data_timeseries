import os
import tempfile

from openpyxl import load_workbook
from utils import WWW, JSONFile, Log

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


def download_source() -> str:
    URL_DOWNLOAD = 'https://data.adb.org/media/10061/download'
    excel_path = tempfile.NamedTemporaryFile(suffix='.xlsx').name
    WWW.download_binary(URL_DOWNLOAD, excel_path)
    log.info(f'Downloaded {URL_DOWNLOAD} to {excel_path}')
    return excel_path


def parse_row(
    worksheet, i_row, year_list, indent_to_text, category1, last_unit
):
    category_str = worksheet.cell(row=i_row, column=I_COL_CATEGORY).value

    data = {}
    for i_year, year in enumerate(year_list):
        value = worksheet.cell(row=i_row, column=3 + i_year).value
        data[year] = parse_number(str(value))

    data = dict([item for item in data.items() if item[1] is not None])

    # data reading complete
    i_row += 1

    if not category_str:
        return None, i_row, indent_to_text, category1, last_unit

    if '(' in category_str:
        last_unit = category_str.split('(')[1].split(')')[0]

    first_word = category_str.split(' ')[0]
    if first_word.isupper() and first_word not in ['GDP', 'GNI']:
        category1 = category_str.strip()
        return None, i_row, indent_to_text, category1, last_unit

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

    if last_unit in category or last_unit in sub_category:
        unit = last_unit
    else:
        unit = DEFAULT_UNIT

    n_non_none = sum(1 for v in data.values() if v is not None)
    if n_non_none == 0:
        return None, i_row, indent_to_text, category1, last_unit

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
    return d, i_row, indent_to_text, category1, last_unit


def parse_excel(excel_path: str):
    workbook = load_workbook(excel_path)
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
    MAX_ROWS = 1_000
    while i_row < MAX_ROWS:
        d, i_row, indent_to_text, category1, last_unit = parse_row(
            worksheet, i_row, year_list, indent_to_text, category1, last_unit
        )
        d_list.append(d)
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


def build_data():
    dir_output = init_dir()
    excel_path = download_source()
    d_list = parse_excel(excel_path)
    build_details(d_list, dir_output)


if __name__ == '__main__':
    download_source()
