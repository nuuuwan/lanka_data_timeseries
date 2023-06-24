from selenium.webdriver.common.by import By
from utils import Log

from cbsl.constants import URL_ERESEARCH
from cbsl.edl.Config import Config
from utils_future import Webpage

log = Log(__name__)


class PageSearchCriteria(Webpage):
    def __init__(self, config: Config):
        super().__init__(URL_ERESEARCH)
        self.config = config

    def select_all_subjects(self):
        elem_input_select_all = self.find_element(
            By.ID, 'ContentPlaceHolder1_btnSelectAll'
        )
        elem_input_select_all.click()
        log.debug('Clicked Select All.')

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

    def input_from(self):
        elem_input_from = self.find_element(
            By.ID, 'ContentPlaceHolder1_txtYearFrom'
        )
        elem_input_from.send_keys(self.config.frequency.from_str)
        log.debug(f'Typed "{self.config.frequency.from_str}".')

    def input_to(self):
        elem_input_to = self.find_element(
            By.ID, 'ContentPlaceHolder1_txtYearTo'
        )
        elem_input_to.send_keys(self.config.frequency.to_str)
        log.debug(f'Typed "{self.config.frequency.to_str}".')

    def click_next(self):
        self.sleep(3)
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
        self.input_from()
        self.input_to()

        self.click_next()

        return self
