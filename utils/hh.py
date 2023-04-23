import json
import requests
from utils.no_vac_error import NoVacationError
from utils.engine_classes import Engine
from utils.connector import Connector


class HH(Engine):
    """Class HH for working with hh.ru.
    Methods:
    - get_request(self, keywords: str = "",
                    area: int = 113,
                    page: int = 0,
                    per_page: int = 100) -> None: The method sends
    a GET request to the site and returns data in JSON format
    - get_connector(file_name: str) -> Connector:
        Returns the instance of class Connector
    """

    def __init__(self) -> None:
        """Инициализация объекта класса HH"""
        pass

    def get_request(self, keywords: str = "",
                    area: int = 113,
                    page: int = 0,
                    per_page: int = 100) -> list:
        """The method sends a GET request to the site and returns data
        in JSON format.
        Attributes:
        - keywords: str - keyword for job search
        - area: str|i-the name of the city to search for or its ID
        (113 - region Russia, 1 - Moscow, 1202 -Novosibirsk)
        - page: int - page number of the search result
        - per_page: int - number of results per search page.
        """
        self.keywords = keywords
        self.count = per_page
        self.page = page
        self.area = area
        list_vacations = []
        is_response_successful = False
        for i in range(5):
            self.page = i

            # getting query params
            params = {
                'per_page': self.count,
                'text': self.keywords,
                'page': self.page,
                'User-Agent': 'MyApp/1.0 (something@useful.com)',
                'area': self.area
                }

            url = "https://api.hh.ru/vacancies"
            response = requests.get(url, params=params)

            if response.status_code:
                is_response_successful = True
                text_json = json.loads(response.text)
                if "bad_argument" in text_json:
                    raise NoVacationError(f"Ошибочный ответ {text_json}")
                else:
                    vacancies = text_json["items"]
                    if len(vacancies):
                        for vacancy in vacancies:
                            list_vacations.append(vacancy)
            if not is_response_successful:
                raise ConnectionError(response, response.text)
        if len(list_vacations):
            return list_vacations
        else:
            raise NoVacationError(f"Вакансий с заданными параметрами не\
 найдено:\nkeywords={keywords}, area={self.area},\
 page={page}, count={self.count}")

    @staticmethod
    def get_connector(file_name: str) -> Connector:
        """ Returns the instance of class Connector"""
        connector = Connector(file_name)
        return connector
