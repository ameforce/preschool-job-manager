from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from PreschoolException import PreschoolLessPrintListException
from PreschoolException import PreschoolNotSetRegionException, PreschoolExtractRegionException, PreschoolNoSuchRegion
from PreschoolException import PreschoolNotSetMainInfoException
from PreschoolException import PreschoolNotSetSubregionException
from PreschoolException import PreschoolNotSetProfessionException
from tqdm import tqdm
import os


class PreschoolJobManager:
    def __init__(self, default_url: str = 'https://www.gogane.kr/c/main.cgi?board=gi2'):
        self.__driver = webdriver.Chrome()
        self.__default_url = default_url
        self.__region_list = None
        self.__main_info_element_list = None
        self.__main_info_element_length = 0
        self.__subregion_list = None
        self.__profession_list = None
        self.__facilities_list = None
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

    def __get_element(self, element_xpath: str, frame_name: str = None, implicitly_wait: float = 2) -> WebElement:
        self.__driver.implicitly_wait(implicitly_wait)
        if self.__switch_frame(frame_name):
            try:
                element = self.__driver.find_element(By.XPATH, element_xpath)
                return element
            except NoSuchElementException:
                raise NoSuchElementException

    def __get_elements(self, element_xpath: str, frame_name: str = None, implicitly_wait: float = 2) -> list[WebElement]:
        self.__driver.implicitly_wait(implicitly_wait)
        if self.__switch_frame(frame_name):
            try:
                element_list = self.__driver.find_elements(By.XPATH, element_xpath)
                return element_list
            except NoSuchElementException:
                raise NoSuchElementException

    @staticmethod
    def print_and_selection(print_list: list[str], print_msg: str = '원하는 번호를 골라주세요') -> int:
        if print_list is None or len(print_list) <= 1:
            raise PreschoolLessPrintListException
        print(print_msg)
        for i in range(len(print_list)):
            print(f'{i + 1}. {print_list[i]}')
        choose_num = int(input('--> '))
        return choose_num

    def extract_region_list(self) -> list[str]:
        element_list: list[WebElement] = []
        element_length = 0
        while True:
            try:
                element_list = self.__get_elements('/html/body/div/table/tbody/tr[1]/td[1]/a',
                                                   implicitly_wait=0)
                element_length = len(element_list)
                break
            except NoSuchElementException:
                continue
        region_list = []
        for i in range(element_length):
            region_list.append(element_list[i].text)
        if len(region_list) <= 1:
            raise PreschoolExtractRegionException
        return region_list

    def get_region_list(self) -> list[str]:
        if self.__region_list is None:
            raise PreschoolNotSetRegionException
        return self.__region_list

    def set_region_list(self, region_list: list[str]) -> None:
        self.__region_list = region_list
        return

    def browser_select_region(self, region_num: int) -> None:
        try:
            self.__get_element(f'/html/body/div/table/tbody/tr[1]/td[1]/a[{region_num}]').click()
        except NoSuchElementException:
            raise PreschoolNoSuchRegion
        return

    def extract_main_info_element_list(self) -> list[WebElement]:
        element_list: list[WebElement] = []
        while True:
            try:
                element_list = self.__get_elements('/html/body/div/table/tbody/tr[1]/td[1]/table[2]/tbody/tr',
                                                   implicitly_wait=0)
                break
            except NoSuchElementException:
                continue
        return element_list

    def set_main_info_element_list_and_length(self, main_info_element_list: list[WebElement]) -> None:
        self.__main_info_element_list = main_info_element_list
        self.__main_info_element_length = len(main_info_element_list)
        return

    def extract_subregion_list(self) -> list[str]:
        if self.__main_info_element_list is None:
            raise PreschoolNotSetMainInfoException
        os.system('cls')
        subregion_list = []
        for i in tqdm(range(self.__main_info_element_length), desc='세부 지역 추출 작업'):
            try:
                self.__main_info_element_list[i].find_element(By.XPATH, 'td[1]/b')
                continue
            except NoSuchElementException:
                refine_element = self.__main_info_element_list[i].find_element(By.XPATH, 'td[1]')
                if refine_element.text != '' and refine_element.text not in subregion_list:
                    subregion_list.append(refine_element.text)
        subregion_list.pop(0)
        return subregion_list

    def get_subregion_list(self) -> list[str]:
        if self.__subregion_list is None:
            raise PreschoolNotSetSubregionException
        return self.__subregion_list

    def set_subregion_list(self, subregion_list: list[str]) -> None:
        self.__subregion_list = subregion_list
        return

    def extract_profession_list(self) -> list[str]:
        if self.__main_info_element_list is None:
            raise PreschoolNotSetMainInfoException
        os.system('cls')
        profession_list = []
        for i in tqdm(range(self.__main_info_element_length), desc='직종 추출 작업'):
            try:
                self.__main_info_element_list[i].find_element(By.XPATH, 'td[2]/b')
                continue
            except NoSuchElementException:
                try:
                    refine_element = self.__main_info_element_list[i].find_element(By.XPATH, 'td[2]')
                    if refine_element.text != '' and refine_element.text not in profession_list:
                        profession_list.append(refine_element.text)
                except NoSuchElementException:
                    continue
        profession_list.pop(0)
        return profession_list

    def get_profession_list(self) -> list[str]:
        if self.__profession_list is None:
            raise PreschoolNotSetProfessionException
        return self.__profession_list

    def set_profession_list(self, profession_list: list[str]) -> None:
        self.__profession_list = profession_list
        return

    def extract_facilities_list(self) -> list[str]:
        if self.__main_info_element_list is None:
            raise PreschoolNotSetMainInfoException
        os.system('cls')
        facilities_list = []
        for i in tqdm(range(self.__main_info_element_length), desc='시설 추출 작업'):
            try:
                self.__main_info_element_list[i].find_element(By.XPATH, 'td[4]/b')
                continue
            except NoSuchElementException:
                try:
                    refine_element = self.__main_info_element_list[i].find_element(By.XPATH, 'td[4]')
                    if refine_element.text != '' and refine_element.text not in facilities_list:
                        facilities_list.append(refine_element.text)
                except NoSuchElementException:
                    continue
        facilities_list.pop(0)
        return facilities_list

    def get_facilities_list(self) -> list[str]:
        if self.__facilities_list is None:
            raise PreschoolNotSetProfessionException
        return self.__facilities_list

    def set_facilities_list(self, facilities_list: list[str]) -> None:
        self.__facilities_list = facilities_list
        return
