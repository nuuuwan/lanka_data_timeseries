import os
import tempfile

from selenium.webdriver.common.by import By
from utils import JSONFile, Log

from lanka_data_timeseries.cbsl.Config import Config
from lanka_data_timeseries.cbsl.DataBuilder import DataBuilder
from utils_future import WebpageWrapper

log = Log(__name__)


def clean_str(x):
    x = x.replace('"', '')
    x = x.replace('%', 'Pct.')
    x = x.replace('/', ' or ')
    x = x.replace(':', '_')
    return x


class PageSearchResult(WebpageWrapper):
    def __init__(self, webpage, config: Config):
        super().__init__(webpage)
        self.config = config

    @staticmethod
    def parse_tds(elem_td_list, d_idx, category, time_list):
        cells = [elem_td.text for elem_td in elem_td_list]
        row_num = cells[0].strip()
        if row_num == '':
            category = clean_str(cells[1])
            if category not in d_idx:
                d_idx[category] = {}
        else:
            sub_category = clean_str(cells[1])
            if sub_category not in d_idx[category]:
                d_idx[category][sub_category] = dict(
                    unit=cells[2], scale=cells[3], data={}
                )
            for time_i, cell in zip(time_list, cells[4:]):
                d_idx[category][sub_category]['data'][time_i] = cell
        return d_idx, category

    def parse_table(self):
        elem_table = self.find_element(By.ID, 'ContentPlaceHolder1_grdResult')
        elem_tbody = elem_table.find_element(By.TAG_NAME, 'tbody')
        elem_tr_list = elem_tbody.find_elements(By.TAG_NAME, 'tr')
        n = len(elem_tr_list)
        log.debug(f'Found {n} rows.')

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

    def parse_footnote_table(self):
        elem_table = self.find_element(
            By.ID, 'ContentPlaceHolder1_grdFootNotes'
        )
        elem_tbody = elem_table.find_element(By.TAG_NAME, 'tbody')
        elem_tr_list = elem_tbody.find_elements(By.TAG_NAME, 'tr')
        n = len(elem_tr_list)
        log.debug(f'Found {n} footnote rows.')

        d_footnote_idx = {}
        sub_category = None
        for elem_tr in elem_tr_list:
            elem_td_list = elem_tr.find_elements(By.TAG_NAME, 'td')
            elem_data_td = elem_td_list[-1]
            td_text = elem_data_td.text
            elem_span = elem_data_td.find_element(By.TAG_NAME, 'span')
            style = elem_span.get_attribute("style")
            if 'bold' in style:
                sub_category = td_text.partition(')')[-1].strip()
                d_footnote_idx[sub_category] = {}
            else:
                tokens = td_text.split(':')
                if len(tokens) == 2:
                    k = tokens[0].strip()
                    v = tokens[1].strip()
                    d_footnote_idx[sub_category][k] = v
        return d_footnote_idx

    @staticmethod
    def write(d_idx):
        dir_latest = os.path.join(
            tempfile.gettempdir(), 'tmp.lanka_data_timeseries', 'latest'
        )

        if not os.path.exists(dir_latest):
            os.makedirs(dir_latest)
            log.debug(f'Created {dir_latest}')

        for category, d_sub in d_idx.items():
            for sub_category, d_data in d_sub.items():
                log.debug(f'Writing {category}.{sub_category}...')
                file_name = os.path.join(
                    dir_latest, f'{category}.{sub_category}.json'
                )
                JSONFile(file_name).write(d_data)
                log.debug(f'Wrote {file_name}')

    def extract_table(self):
        d_idx = self.parse_table()
        d_footnote_idx = self.parse_footnote_table()
        PageSearchResult.write(d_idx)
        DataBuilder(d_idx, d_footnote_idx, self.config).write()

    def run(self):
        log.info('STEP 3️⃣) Running PageSearchResult.')

        current_url = self.driver.current_url
        log.debug(f'{current_url=}')

        self.extract_table()

        return self
