# Парсер вакансий

Проект __Парсер вакансий__ создан для работы с API сайта hh.ru.
Полученные данные с сайта hh.ru сохраняются в базу данных Posgresql.
Для заполнения базы данных требуется файл data\favorits_ employers.json, содержащий список работодателей в формате json, для которых будет формироваться запрос к сайту hh.ru.

Пример файла:

    [
        {"id": "3529", "name": "СБЕР"},
        {"id": "2180", "name": "Ozon"},
        {"id": "9211299", "name": "Онлайн-школа программирования КиберУм"},
        {"id": "2657797", "name": "Алгоритмика"}
    ]
Поле id является обязательным, т. к по id осуществляется поиск работодателя.

Для корректного подключения к базе данных настройки для подключения должны находится в файле
database.ini в корневом каталоге проекта. Файл дожен иметь следующую структуру:

    [postgresql]
        host=<имя хоста>
        user=<имя пользователя базы данных>
        password=<пароль>
        port=<порт>

Для работы проекта реализованы следующие классы.


## Класс DBManager
__Класс DBManager__ служит для подключения к БД Postgres.
По умолчанию название базы данных - vacancies. Любое  другое можно задать при инициализации, передав араметр database_name.
Параметры инициализации базы данный задаются в файле database.ini.

Методы:
*   get_companies_and_vacancies_count(): получает список всех компаний
     и количество вакансий у каждой компании.
*   get_all_vacancies(): получает список всех вакансий с указанием
     названия компании, названия вакансии и зарплаты и ссылки на вакансию.
*   get_avg_salary(): получает среднюю зарплату по вакансиям.
*   get_vacancies_with_higher_salary(): получает список всех вакансий,
     у которых зарплата выше средней по всем вакансиям.
*   get_vacancies_with_keyword(): получает список всех вакансий,
     в названии которых содержатся переданные в метод слова, например 'python'.
*   _print_table() - печатает все данные из таблицы, название которой в нее
    передано

## Класс Connector
__Класс Connector__ реализует доступ к файлу. Инициализируется строкой, содержащей путь к файлу. Файл должен содержать данные в json формате.

Methods:
*   is_valid_json: bool - cheking if file is in JSON-format.
*   is_file_exist: bool -cheking if file exists
*   read_file: str - getting text from file data_file
*   is_file_not_old: bool - checking if file not older than number days
*   save_date: str - saving data in file data_file
*   insert: dict | list - insert data in file with saving it's structure.
*   select: list | KeyError - selecting dates from file.
        The key is the field for filtering. The value is the desired value.
*   delete: list | KeyError - deleting date, using query.

    Atributes:

*   data_file:str - the path to the json-file. It has getter and setter.
*   text: str - the text from the file
*   save_date: list - list for saving in file
*   delete_query: dict - dict for deleting data
*   select_query: dict - dict for selection data
*   days_outdate: int - the number of days after which the file
    is outdated

## Класс Vacancy
__Класс Vacancy__ представляет объект для работы с вакансией.

Atributes:

*   id:int -  id of the vacancy on the source site,
*   title:str - job title,
*   salary_from: float - minimum salary level,
*   salary_to: float - maximum salary level,
*   url:str - vacancy address,
*   description:str -  job description,
*   firm_name:str -name of the employer organization,
*   service:str- the name of the site from which vacancies were received.
    Takes the values HH and SJ.

## Класс HH
__Класс HH__ создан для работы с сайтом hh.ru.

Methods:

*   get_request(self, keywords: str = "",
                    area: int = 113,
                    per_page: int = 100,
                    page: int = 0,) -> None: The method sends a GET request to the site and returns data
        in JSON format
*   get_connector(file_name: str) -> Connector:
        Returns the instance of class Connector

## Класс HH_sql
__Класс HH_sql__ унаследован от класса HH.

Методы, которые были добавлены::

*   get_connectordb(file_name: str) -> DBmanager:
        возвращает экземпляр класса DBmanager

*   get_request_employers_vacancies() -> list:
    Возвращает список вакансий для данного работодателя по его id.

*   get_request_employers() -> dict:
    Возвращает данные для работодателя по его id



## Класс NoVacationError
__Класс NoVacationError__ создан для обработки исключения, которое выбрасывается в случае, если при запросе к сайту с вакансиями ни одна не найдена.

## Класс Employer
__Класс Employer__ для представления данных работодателя

Атрибуты:
*   id
*   name
*   description
*   url
*   alternate_url
*   trusted


## Функции
*   def get_employer_from_json(data: dict) -> Employer:
    функция получает словарь и возвращает объект Employer, заполненный данными из словаря
*   get_vacancy_from_json(vacancy: dict) -> Vacancy_sql:
функция возвращает объект Vacancy_sql, заполненный данными из словаря

## Работа с программой

Ключевое слово (keyword) и путь к файлу (file_path) с данными для поиска вакансии задаются в файле config.py.
При запуске появляется меню

    ------Парсер вакансий------
    1 - Сделать запрос на сайт hh.ru по списку работодателей и сохранить данные в базе данных
    2 - Получить данные из базы данных
    3 - Выход.

При выборе пункта 1  данные с сайта hh.ru будeт выполнен запрос на сайт hh.ru для работодателей из файла data\favorits_ employers.json.


При выборе пункта 2 появится меню

    Выберите нужное действие:
    1 - Посчитать вакансии у каждого работодателя
    2 - Вывести среднюю зарплату
    3 - Вывести список всех вакансий
    4 - Вывести список всех вакансий, у которых зарплата выше средней
    5 - Вывести список всех вакансий, в названии которых содержится ключевое слово
    6 - Возврат в главное меню.