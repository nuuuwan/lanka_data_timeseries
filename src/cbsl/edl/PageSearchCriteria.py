from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import Log

from cbsl.constants import URL_ERESEARCH
from cbsl.edl.Frequency import Frequency
from utils_future import Webpage

log = Log(__name__)


class PageSearchCriteria(Webpage):
    def __init__(self, frequency: str):
        super().__init__(URL_ERESEARCH)
        self.frequency = frequency

    def select_all_subjects(self):
        elem_input_select_all = self.find_element(
            By.ID, 'ContentPlaceHolder1_btnSelectAll'
        )
        elem_input_select_all.click()
        log.debug('Clicked Select All.')

    def select_time_search_criteria(self):
        elem_select_frequency = self.find_element(
            By.ID, 'ContentPlaceHolder1_drpFrequency'
        )
        elem_option = elem_select_frequency.find_element(
            By.XPATH, f"//option[@value='{self.frequency.value}']"
        )
        elem_option.click()
        log.debug(f'Selected {self.frequency.name}.')

    def input_from(self):
        elem_input_from = self.find_element(
            By.ID, 'ContentPlaceHolder1_txtYearFrom'
        )
        elem_input_from.send_keys(self.frequency.from_str)
        elem_input_from.send_keys(Keys.ENTER)
        log.debug(f'Typed "{self.frequency.from_str}".')

    def input_to(self):
        elem_input_to = self.find_element(
            By.ID, 'ContentPlaceHolder1_txtYearTo'
        )
        elem_input_to.send_keys(self.frequency.to_str)
        elem_input_to.send_keys(Keys.ENTER)
        log.debug(f'Typed "{self.frequency.to_str}".')

    def click_next(self):
        elem_input_next = self.find_element(
            By.ID, 'ContentPlaceHolder1_btnNext'
        )
        elem_input_next.click()
        log.debug('Clicked Next.')

    def run(self):
        self.open()

        self.select_all_subjects()
        self.select_time_search_criteria()
        self.input_from()
        self.input_to()
        self.click_next()

        self.sleep(5)

        self.screenshot(force_nocache=True)
        self.close()


if __name__ == '__main__':
    PageSearchCriteria(Frequency.ANNUAL).run()
