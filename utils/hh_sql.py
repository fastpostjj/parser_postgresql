import json
import requests
from utils.no_vac_error import NoVacationError
from utils.dbmanager import DBManager
from utils.employer import Employer
from utils.hh import HH


class HH_sql(HH):
    """Class HH_sql for working with hh.ru.
    Methods:
    
    - get_connectordb(file_name: str) -> DBmanager:
        Returns the instance of class DBmanager

    - get_request_employers_vacancies() -> list:
     Возвращает список вакансий для данного работодателя по его id.
        The method sends a GET request to the site and returns
        the employer's data using  employer_id in JSON format.
        Attributes:
        - employer_id: int | str - id for searchig  the employer
        - keywords: str - keyword for job search
        - area: str|i-the name of the city to search for or its ID
    - get_request_employers() -> dict:
    Возвращает данные для работодателя по его id
        The method sends a GET request to the site and returns data
        in JSON format.
        Attributes:
       - employer_id: int| str - id for searching employers

    """

    def __init__(self) -> None:
        """Инициализация объекта класса HH"""
        pass

    def get_request_employers_vacancies(self,  employer_id,
    keywords: str = "",
    area: int = 113,
    page: int = 0,
    per_page: int = 100
    ) -> list:
        """
        Возвращает список вакансий для данного работодателя по его id.
        The method sends a GET request to the site and returns
        the employer's data using  employer_id in JSON format.
        Attributes:
        - employer_id: int | str - id for searchig  the employer
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
        list_vacancies = []
        is_response_successful = False

        # getting query params
        params = {
                'per_page': self.count,
                'text': self.keywords,
                'page': self.page,
                'User-Agent': 'MyApp/1.0 (something@useful.com)',
                'area': self.area,
                'only_with_vacancies': True
                }

        url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"

        response = requests.get(url, params=params)

        if response.status_code:
            is_response_successful = True
            text_json = json.loads(response.text)
            if not "items" in text_json:
                raise NoVacationError(f"Ошибочный ответ {text_json}")
            else:
                vacancies = text_json["items"]
                if len(vacancies):
                    for vacancy in vacancies:
                        list_vacancies.append(vacancy)
        if not is_response_successful:
            raise ConnectionError(response, response.text)
        if len(list_vacancies):
            return list_vacancies
        else:
            raise NoVacationError(f"Вакансий с заданными параметрами не\
 найдено:\nemployer_id={employer_id}, keywords={keywords}, area={self.area},\
 page={page}, count={self.count}")

    def get_request_employers(self, employer_id: int| str) -> dict:
        """The method sends a GET request to the site and returns data
        in JSON format.
        Attributes:
       - employer_id: int| str - id for searching employers
        """

        is_response_successful = False

        params = {
            'User-Agent': 'MyApp/1.0 (something@useful.com)',
            # 'only_with_vacancies': True
            }

        url = f"https://api.hh.ru/employers/{employer_id}"

        try:
            response = requests.get(url, params=params)
        except Exception as error:
            print(error)

        if response.status_code:
            is_response_successful = True
            text_json = json.loads(response.text)
            if not "id" in text_json:
                raise NoVacationError(f"Ошибочный ответ {text_json}")
            else:
                employers = text_json
        if not is_response_successful:
            raise ConnectionError(response, response.text)
        if len(employers):
            return employers
        else:
            raise NoVacationError(f"Работодателей с заданными параметрами не\
 найдено:\nemployer_id={employer_id}, keywords={keywords}, area={self.area},\
 page={page}, count={self.count}")

    @staticmethod
    def get_connectordb() -> DBManager:
        """ Returns the instance of class DBManager"""
        connectordb = DBManager()
        return connectordb