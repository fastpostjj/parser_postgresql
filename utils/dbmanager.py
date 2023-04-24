import psycopg2
from psycopg2 import Error
# from config import database_name, config
from config import config
from utils.vacancy_sql import Vacancy_sql
from utils.employer import Employer
from utils.func import get_vacancy_from_json


class DBManager():
    """## Класс DBManager для подключения к БД Postgres.
    По умолчанию название базы данных - vacancies. Любое другое можно задать
    при инициализации, передав параметр database_name.
    Параметры инициализации базы данный задаются в файле database.ini, имеющим
    следующую структуру:
    [postgresql]
    host=<имя хоста>
    user=<имя пользователя базы данных>
    password=<пароль>
    port=<порт>

    Методы:
    - get_companies_and_vacancies_count(): получает список всех компаний
     и количество вакансий у каждой компании.
    - get_all_vacancies(): получает список всех вакансий с указанием
     названия компании, названия вакансии и зарплаты и ссылки на вакансию.
    - get_avg_salary(): получает среднюю зарплату по вакансиям.
    - get_vacancies_with_higher_salary(): получает список всех вакансий,
     у которых зарплата выше средней по всем вакансиям.
    - get_vacancies_with_keyword(): получает список всех вакансий,
     в названии которых содержатся переданные в метод слова, например 'python'.
    - _print_table() - печатает все данные из таблицы, название которой в нее
    передано
    - change_apostrophe() - для корректного добавления текста
    в базу postgresql заменяет одинарную кавычку на двойную
    - is_param_correct() - проверяет наличие в атрибуте param всех
    необходимых ключей для подключения к базе данных
    """

    def __init__(self, database_name='vacancies'):
        """ Инициализация экземпляра класса DBManager
        """
        self.database_name = database_name
        self.param = self.get_config()
        self.conn = psycopg2.connect(
            database=self.database_name,
            **self.param
            )

    def get_config(self):
        param = config()
        if not self.is_param_correct(param):
            raise KeyError
        return param

    @staticmethod
    def is_param_correct(param) -> bool:
        """checking if dict param contains all keys:
        host, user, password, port

        """
        is_correct = True
        if "host" not in param:
            is_correct = False
        if "user" not in param:
            is_correct = False
        if "password" not in param:
            is_correct = False
        if "port" not in param:
            is_correct = False
        return is_correct

    @staticmethod
    def change_apostrophe(text: str) -> str:
        return text.replace("'", "''")

    def create_tables(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                create_text = '''
                DROP TABLE IF EXISTS vacancies;
                DROP TABLE IF EXISTS employers;
                CREATE TABLE employers(
                    employer_id varchar(20) PRIMARY KEY,
                    employer_name varchar(100) NOT NULL,
                    description text,
                    employer_url varchar(100),
                    alternate_url varchar(100),
                    trusted boolean
                    );\n'''
                cur.execute(create_text)

                create_text = '''
                CREATE TABLE vacancies(
                    vacancy_id varchar(20) PRIMARY KEY,
                    vacancy_employer_id varchar(20),
                    FOREIGN KEY (vacancy_employer_id) REFERENCES employers(employer_id),
                    vacancy_name varchar(100) NOT NULL,
                    vacancy_area varchar(100),
                    vacancy_salary_from real,
                    vacancy_salary_to real,
                    vacancy_salary real,
                    vacancy_salary_currency varchar(20),
                    vacancy_salary_gross boolean,
                    vacancy_published_at date,
                    vacancy_url varchar(100),
                    vacancy_requirement text,
                    vacancy_responsibility text,
                    vacancy_contacts varchar(100),
                    vacancy_experience varchar(100),
                    vacancy_employment varchar(100));
                    '''
                cur.execute(create_text)

    def _print_table(self, table_name):
        """Printing all row from table
        """
        with psycopg2.connect(
            database=self.database_name,
            **self.param
            ) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {table_name};")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def insert_employer(self, employer: Employer) -> Employer | None:
        insert_text = '''
                    INSERT INTO
                    employers(employer_id, employer_name, description,
                    employer_url, alternate_url, trusted) ''' +\
                    f'''VALUES ('{employer.id}', '{employer.name}',\
 '{self.change_apostrophe(employer.description)}', \
'{employer.url}', '{employer.alternate_url}',{employer.trusted})
                    ON CONFLICT (employer_id) DO NOTHING;'''

        with self.conn as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(insert_text)
                    conn.commit()
                    return employer
            except Exception as error:
                print(error)
                print(insert_text)

    def insert_vacancies(self, vacancy: Vacancy_sql) -> Vacancy_sql | None:
        with self.conn as conn:
            try:
                with conn.cursor() as cur:
                    insert_text = '''
                    INSERT INTO vacancies(vacancy_id, vacancy_name, vacancy_employer_id, vacancy_area, vacancy_salary_from,
                    vacancy_salary_to, vacancy_salary, vacancy_salary_currency, vacancy_salary_gross,
                    vacancy_published_at, vacancy_url,
                    vacancy_requirement,
                    vacancy_responsibility,
                    vacancy_contacts, vacancy_experience, vacancy_employment)
                    VALUES ('%s', '%s', '%s', '%s', %s, %s, %s, '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                    ON CONFLICT (vacancy_id) DO NOTHING;''' %(
                        vacancy.id,
                        vacancy.name,
                        vacancy.vacancy_employer_id,
                        vacancy.area,
                        vacancy.salary_from,
                        vacancy.salary_to,
                        vacancy.salary,
                        vacancy.salary_currency,
                        vacancy.salary_gross,
                        vacancy.published_at,
                        vacancy.url,
                        self.change_apostrophe(vacancy.requirement) if vacancy.requirement else "",
                        self.change_apostrophe(vacancy.responsibility) if vacancy.responsibility else "",
                        vacancy.contacts,
                        self.change_apostrophe(vacancy.experience) if vacancy.experience else "",
                        self.change_apostrophe(vacancy.employment) if vacancy.employment else ""
                        )
                    # print(insert_text)
                    cur.execute(insert_text)
                    conn.commit()
                    return vacancy
            except Exception as error:
                print(error)
                print(insert_text)

    def get_companies_and_vacancies_count(self) -> list:
        '''
        получает список всех компаний и количество вакансий у каждой компании
        '''
        query_text = """
        SELECT employer_name, COUNT(*)
        FROM vacancies
		JOIN employers ON (vacancies.vacancy_employer_id=employers.employer_id)
        GROUP BY employer_name;
        """
        with self.conn as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(query_text)
                    conn.commit()
                    rows = cur.fetchall()
                    return rows
            except Exception as error:
                print(error)

    def get_all_vacancies(self) -> list:
        '''получает список всех вакансий с указанием названия
        компании, названия вакансии и зарплаты и ссылки на вакансию
        '''
        query_text = """
        SELECT employer_name, vacancy_name, vacancy_salary_from,
        vacancy_salary_to, vacancy_salary_currency, vacancy_url
        FROM vacancies
        JOIN employers ON (vacancies.vacancy_employer_id=employers.employer_id);
        """
        with self.conn as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(query_text)
                    conn.commit()
                    rows = cur.fetchall()
                    return rows
            except Exception as error:
                print(error)

    def get_avg_salary(self) -> int:
        """получает среднюю зарплату по вакансиям
        """
        query_text = """
            SELECT ROUND(AVG(vacancy_salary))--  FROM vacancies;
            FROM vacancies;
            """
        with self.conn as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(query_text)
                    conn.commit()
                    rows = cur.fetchall()
                    return rows[0][0]
            except Exception as error:
                print(error)

    def get_vacancies_with_higher_salary(self) -> list:
        ''' получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям
        '''
        query_text = """
            SELECT *
            FROM vacancies
            WHERE vacancy_salary>
            (SELECT AVG(vacancy_salary)
            FROM vacancies);
            """
        with self.conn as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(query_text)
                    conn.commit()
                    rows = cur.fetchall()
                    return rows
            except Exception as error:
                print(error)

    def get_vacancies_with_keyword(self, text: str) -> list:
        '''получает список всех вакансий, в названии которых содержатся переданные
        в метод слова, например “python”
        '''
        query_text = f"""
            SELECT *
            FROM vacancies
            WHERE vacancy_name LIKE '%{text}%'
            """
        with self.conn as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(query_text)
                    conn.commit()
                    rows = cur.fetchall()
                    return rows
            except Exception as error:
                print(error)
