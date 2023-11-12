from lib.LogManager.LogManager import LogManager


class PreschoolLessPrintListException(Exception):
    def __init__(self) -> None:
        self.__loger = LogManager()
        self.__loger.log('목록이 1개 이하이기 때문에 선택할 필요가 없습니다.', 'ERROR')
        return


class PreschoolNotSetRegionException(Exception):
    def __init__(self) -> None:
        self.__loger = LogManager()
        self.__loger.log('지역이 설정되지 않았습니다.', 'ERROR')
        return


class PreschoolExtractRegionException(Exception):
    def __init__(self) -> None:
        self.__loger = LogManager()
        self.__loger.log('지역이 부족하게 추출 되었습니다.', 'ERROR')
        return


class PreschoolNotSetMainInfoException(Exception):
    def __init__(self) -> None:
        self.__loger = LogManager()
        self.__loger.log('주요 정보가 설정되지 않았습니다.', 'ERROR')
        return


class PreschoolNoSuchRegion(Exception):
    def __init__(self) -> None:
        self.__loger = LogManager()
        self.__loger.log('브라우저에서 지역 요소를 찾지 못했습니다.', 'ERROR')
        return


class PreschoolNotSetSubregionException(Exception):
    def __init__(self) -> None:
        LogManager().log('세부 지역이 설정되지 않았습니다.', 'ERROR')
        return


class PreschoolNotSetProfessionException(Exception):
    def __init__(self) -> None:
        LogManager().log('직종이 설정되지 않았습니다.', 'ERROR')
        return
