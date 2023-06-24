from selenium.webdriver.common.by import By
from utils import Log

from utils_future import WebpageWrapper

log = Log(__name__)


class PageSelectItems(WebpageWrapper):
    def click_list_all_items(self):
        self.find_element(By.ID, 'ContentPlaceHolder1_chkshowAll').click()
        log.debug('Clicked "List all items".')

    def select_all_items(self):
        elem_item_list = self.find_elements(By.ID, 'chkSelect')
        n = len(elem_item_list)

        if n == 0:
            raise Exception('No items found.')

        log.debug(f'Found {n} items.')

        for elem_item in elem_item_list:
            elem_item.click()
        log.debug(f'Clicked {n} items.')
        return n

    def click_add(self):
        self.find_element(By.ID, 'add').click()
        log.debug('Clicked "Add".')

    def click_next(self):
        elem_input_next = self.find_element(
            By.ID, 'ContentPlaceHolder1_btnNext'
        )
        elem_input_next.click()
        log.debug('Clicked Next.')

        log.debug('Waiting for New Query...')
        self.find_element(By.ID, 'ContentPlaceHolder1_btnNEwQuery2')

    def remove_footer(self):
        self.driver.execute_script(
            "document.getElementsByClassName('footdiv')[0].remove();"
        )
        log.debug('Removed footer.')

    def run(self):
        log.info('STEP 2️⃣) Running PageSelectItems.')
        current_url = self.driver.current_url
        log.debug(f'{current_url=}')

        self.click_list_all_items()
        self.sleep(3)

        self.remove_footer()
        self.select_all_items()

        self.sleep(3)
        self.click_add()

        self.sleep(3)
        self.click_next()

        return self
