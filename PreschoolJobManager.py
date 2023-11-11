from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
import time


class PreschoolJobManager:
    def __init__(self, default_url: str = 'https://www.gogane.kr/c/main.cgi?board=gi2'):
        self.__driver = webdriver.Chrome()
        self.__default_url = default_url
        self.__region_list = None
        self.__subregion_list = None
        return

    def get_default_url(self) -> str:
        return self.__default_url

    def move_site(self, url: str) -> None:
        self.__driver.get(url)
        return

    def __switch_frame(self, frame_name: str = None) -> bool:
        if frame_name is not None:
            try:
                self.__driver.switch_to.frame(frame_name)
            except NoSuchFrameException:
                try:
                    self.__driver.find_element(By.XPATH, f'//*[@id="{frame_name}"]')
                except NoSuchElementException:
                    return False
        return True

    def __get_element(self, element_xpath: str, frame_name: str = None, implicitly_wait: float = 2) -> WebElement or None:
        self.__driver.implicitly_wait(implicitly_wait)
        element = None
        if self.__switch_frame(frame_name):
            try:
                element = self.__driver.find_element(By.XPATH, element_xpath)
            except NoSuchElementException:
                pass
        return element

    def extract_region_list(self) -> list[str]:
        region_list = []
        i = 1
        while True:
            element = self.__get_element(f'/html/body/div/table/tbody/tr[1]/td[1]/a[{i}]')
            if element is None:
                break
            region_list.append(element.text)
            i += 1
        return region_list

    def get_region_list(self) -> list[str]:
        return self.__region_list

    def set_region_list(self, region_list: list[str]) -> None:
        self.__region_list = region_list
        return

    def print_and_region_chooser(self) -> int:
        if self.__region_list is None:
            raise Exception('지역이 설정되지 않았습니다.\n지역을 먼저 설정해야 사용 가능합니다.')
        print('원하는 지역을 선택해주세요')
        for i in range(len(self.__region_list)):
            print(f'{i + 1}. {self.__region_list[i]}')
        choose_num = int(input('-->'))
        return choose_num

    def select_region(self, region_num: int) -> None:
        self.__get_element(f'/html/body/div/table/tbody/tr[1]/td[1]/a[{region_num}]').click()
        return

    def extract_subregion(self) -> list[str]:
        subregion_list = []
        i = 0
        while True:
            # element = self.__get_element(f'/html/body/div/table/tbody/tr[1]/td[1]/table[1]/tbody/tr[{3+i}]/td[1]')
            element = self.__get_element(f'/html/body/div/table/tbody/tr[1]/td[1]/table[2]/tbody/tr[{3+i}]/td[1]/b',
                                         implicitly_wait=0)
            if element is not None:
                i += 1
                continue

            element = self.__get_element(f'/html/body/div/table/tbody/tr[1]/td[1]/table[2]/tbody/tr[{3+i}]/td[1]',
                                         implicitly_wait=0)
            i += 1
            if element is None:
                break
            if element.text == '' or element.text in subregion_list:
                continue
            subregion_list.append(element.text)
            print(f'INFO: {i-1}: {element.text}')
        return subregion_list

    def get_subregion_list(self) -> list[str]:
        return self.__subregion_list

    def set_subregion_list(self, subregion_list: list[str]) -> None:
        self.__subregion_list = subregion_list
        return
