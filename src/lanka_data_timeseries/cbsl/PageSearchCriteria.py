from selenium.webdriver.common.by import By
from utils import Log

from lanka_data_timeseries.cbsl.Config import Config
from lanka_data_timeseries.constants import URL_ERESEARCH
from utils_future import Webpage

log = Log(__name__)


class PageSearchCriteria(Webpage):
    def __init__(self, config: Config):
        super().__init__(URL_ERESEARCH)
        self.config = config

    def select_some_subjects(self, i_start, i_end):
        elem_item_list = self.find_elements(
            By.XPATH, "//input[@type='checkbox']"
        )
        log.debug(f'Found {len(elem_item_list)} subjects.')
        for i in range(i_start, i_end):
            elem_item = elem_item_list[i]
            elem_item.click()
            elem_name = elem_item.get_attribute('name')
            log.debug(f'Clicked {elem_name}')
        log.debug(f'Clicked items {i_start} to {i_end}.')

    def select_time_search_criteria(self):
        elem_select_frequency = self.find_element(
            By.ID, 'ContentPlaceHolder1_drpFrequency'
        )
        elem_option = elem_select_frequency.find_element(
            By.XPATH, f"//option[@value='{self.config.frequency.value}']"
        )
        elem_option.click()
        log.debug(f'Selected {self.config.frequency.name}.')

    def input_text(self, elem_id, text):
        elem = self.find_element(By.ID, elem_id)
        elem.send_keys(text)
        log.debug(f'Typed "{text}" into {elem_id}.')

    def click_next(self):
        self.sleep()
        elem_input_next = self.find_element(
            By.ID, 'ContentPlaceHolder1_btnNext'
        )
        elem_input_next.click()
        log.debug('Clicked Next.')

        log.debug('Waiting for ShowAll...')
        self.find_element(By.ID, 'ContentPlaceHolder1_chkshowAll')

    def run(self):
        log.info('STEP 1️⃣) Running PageSearchCriteria.')
        self.open()
        current_url = self.driver.current_url
        log.debug(f'{current_url=}, {self.config=}')

        self.select_some_subjects(
            self.config.i_subject, self.config.i_subject + 1
        )

        self.select_time_search_criteria()
        for elem_id, text in self.config.frequency.input_text_map.items():
            self.input_text(elem_id, text)

        self.click_next()

        return self
