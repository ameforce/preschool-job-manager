from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
import time


class PreschoolJobManager:
    def __init__(self, default_url: str = 'https://www.gogane.kr/c/main.cgi?board=gi2'):
        self.driver = webdriver.Chrome()
        self.default_url = default_url
        self.region_list = []
        return

    def __move_site(self, url: str) -> None:
        self.driver.get(url)
        return

    def __switch_frame(self, frame_name: str = None) -> bool:
        if frame_name is not None:
            try:
                self.driver.switch_to.frame(frame_name)
            except NoSuchFrameException:
                try:
                    self.driver.find_element(By.XPATH, f'//*[@id="{frame_name}"]')
                except NoSuchElementException:
                    return False
        return True

    def __get_element(self, element_xpath: str, frame_name: str = None, implicitly_wait: float = 2) -> WebElement or None:
        self.driver.implicitly_wait(implicitly_wait)
        element = None
        if self.__switch_frame(frame_name):
            try:
                element = self.driver.find_element(By.XPATH, element_xpath)
            except NoSuchElementException:
                pass
        return element

    def __get_region_list(self) -> list[str]:
        region_list = []
        i = 1
        while True:
            element = self.__get_element(f'/html/body/div/table/tbody/tr[1]/td[1]/a[{i}]')
            if element is None:
                break
            region_list.append(element.text)
            i += 1
        return region_list

    def __set_region_list(self, region_list: list[str]) -> None:
        self.region_list = region_list
        return

    @staticmethod
    def __print_selection(print_list: list[str]) -> None:
        print('원하는 지역을 선택해주세요')
        for i in range(len(print_list)):
            print(f'{i}. {print_list[i]}')
        input('-->')
        return

    def logic(self) -> None:
        self.__move_site(self.default_url)
        self.__set_region_list(self.__get_region_list())
        self.__print_selection(self.__region)
        print(f'region: {self.region_list}')

        time.sleep(5090)
        return