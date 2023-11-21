import os
import tempfile

from openpyxl import load_workbook
from utils import WWW, JSONFile, Log

from lanka_data_timeseries.constants import (DEFAULT_FREQUENCY_NAME,
                                             DIR_TMP_DATA)
from lanka_data_timeseries.other_sources.adb.parsers import (I_ROW_T_HEADER,
                                                             SOURCE_ID,
                                                             parse_row)

log = Log(__file__)


def init_dir():
    dir_output = os.path.join(
        DIR_TMP_DATA,
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
        if d:
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


def build_data():
    dir_output = init_dir()
    excel_path = download_source()
    d_list = parse_excel(excel_path)
    build_details(d_list, dir_output)


if __name__ == '__main__':
    download_source()
