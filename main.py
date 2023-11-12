from PreschoolJobManager import PreschoolJobManager
import time


def main() -> None:
    try:
        pm = PreschoolJobManager()
        pm.move_site(pm.get_default_url())
        pm.set_region_list(pm.extract_region_list())
        pm.browser_select_region(pm.print_and_selection(pm.get_region_list(), '지역을 선택해 주세요'))
        pm.set_main_info_element_list_and_length(pm.extract_main_info_element_list())
        pm.set_subregion_list(pm.extract_subregion_list())
        pm.print_and_selection(pm.get_subregion_list(), '세부 지역을 선택해 주세요')
        pm.set_profession_list(pm.extract_profession_list())
        pm.print_and_selection(pm.get_profession_list(), '직종을 선택해 주세요')
        pm.set_facilities_list(pm.extract_facilities_list())
        pm.print_and_selection(pm.get_facilities_list(), '제외할 유치원을 선택해 주세요.')
        print(pm.get_subregion_list())
        time.sleep(5000)
    except Exception as e:
        print(e)
    return


if __name__ == '__main__':
    main()
