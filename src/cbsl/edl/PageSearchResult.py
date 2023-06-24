import os
import shutil
import tempfile

from selenium.webdriver.common.by import By
from utils import JSONFile, Log, get_time_id

from utils_future import WebpageWrapper

log = Log(__name__)


class PageSearchResult(WebpageWrapper):
    @staticmethod
    def parse_tds(elem_td_list, d_idx, category, time_list):
        cells = [elem_td.text for elem_td in elem_td_list]
        row_num = cells[0].strip()
        if row_num == '':
            category = cells[1]
            if category not in d_idx:
                d_idx[category] = {}
        else:
            sub_category = cells[1]
            if sub_category not in d_idx[category]:
                d_idx[category][sub_category] = dict(
                    unit=cells[2], scale=cells[3], data={}
                )
            for time_i, cell in zip(time_list, cells[4:]):
                d_idx[category][sub_category]['data'][time_i] = cell
        return d_idx, category

    @staticmethod
    def parse_table(elem_tr_list):
        d_idx = {}
        time_list = None
        category = ''
        for elem_tr in elem_tr_list:
            elem_th_list = elem_tr.find_elements(By.TAG_NAME, 'th')
            if elem_th_list:
                time_list = [elem_th.text for elem_th in elem_th_list][4:]

            elem_td_list = elem_tr.find_elements(By.TAG_NAME, 'td')
            if elem_td_list:
                d_idx, category = PageSearchResult.parse_tds(
                    elem_td_list, d_idx, category, time_list
                )

        return d_idx

    @staticmethod
    def write(d_idx):
        dir_tmp_data = os.path.join(
            tempfile.gettempdir(), 'tmp.cbsl', get_time_id()
        )
        if not os.path.exists(dir_tmp_data):
            os.makedirs(dir_tmp_data)
            log.debug(f'Created {dir_tmp_data}')

        for category, d_sub in d_idx.items():
            for sub_category, d_data in d_sub.items():
                file_name = os.path.join(
                    dir_tmp_data, f'{category}.{sub_category}.json'
                )
                JSONFile(file_name).write(d_data)
                log.debug(f'Wrote {file_name}')

        dir_latest = os.path.join(tempfile.gettempdir(), 'tmp.cbsl', 'latest')
        shutil.rmtree(dir_latest)
        shutil.copytree(dir_tmp_data, dir_latest)
        log.debug(f'Copied {dir_tmp_data} to {dir_latest}')

    def extract_table(self):
        elem_table = self.find_element(By.ID, 'ContentPlaceHolder1_grdResult')
        elem_tbody = elem_table.find_element(By.TAG_NAME, 'tbody')
        elem_tr_list = elem_tbody.find_elements(By.TAG_NAME, 'tr')
        n = len(elem_tr_list)
        log.debug(f'Found {n} rows.')

        d_idx = PageSearchResult.parse_table(elem_tr_list)
        PageSearchResult.write(d_idx)

    def run(self):
        log.info('STEP 3️⃣) Running PageSearchResult.')
        current_url = self.driver.current_url
        log.debug(f'{current_url=}')
        self.extract_table()
        return self
