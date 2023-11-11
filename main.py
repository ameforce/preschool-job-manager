from PreschoolJobManager import PreschoolJobManager
import time


def main() -> None:
    try:
        pm = PreschoolJobManager()
        pm.move_site(pm.get_default_url())
        pm.set_region_list(pm.extract_region_list())
        pm.select_region(pm.print_and_region_chooser())
        pm.set_subregion_list(pm.extract_subregion())
        print(pm.get_subregion_list())
        time.sleep(5000)
    except Exception as e:
        print(e)
    return


if __name__ == '__main__':
    main()
