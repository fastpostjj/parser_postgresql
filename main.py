import click
import json
from json import JSONDecodeError
from prettytable import PrettyTable
from utils.dbmanager import DBManager
from config import path_fav_employers
from utils.func import get_employer_from_json, get_vacancy_from_json
from utils.hh_sql import HH_sql


def clrscr():
    # Clear screen using click.clear() function
    click.clear()


def create_tables(dbmanager: DBManager) -> None:
    """Drop tables employers and vacancies and create them
    """
    try:
        dbmanager.create_tables()
    except Exception as error:
        print(error)


def fill_tables(dbmanager: DBManager) -> None:
    """fills tables with getted datas
    """

    hh = HH_sql()

    # готовим файлы для сохранения полученных данных
    # connector_emp = Connector(file_path_emp )
    # connector_vac = Connector(file_path)

    # Читаем список работодаттелей из файла
    with open(path_fav_employers, "r", encoding="utf-8") as file:
        text = file.read()

    # Заполняем базу данных данными
    try:
        list_data = json.loads(text)
        # Сначала заполняем таблицу employers
        for item in list_data:
            employer_dict = hh.get_request_employers(item["id"])
            employer = get_employer_from_json(employer_dict)

            # connector_emp.insert_only_unic(employer_dict)
            dbmanager.insert_employer(employer)

            # Для каждого работодателя выбираем все вакансии
            # и заполняем таблицу vacancies
            list_vacancies = hh.get_request_employers_vacancies(item["id"])
            # connector_vac.insert_only_unic(list_vacancies)
            for vacancy_dict in list_vacancies:
                vacancy = get_vacancy_from_json(vacancy_dict)
                dbmanager.insert_vacancies(vacancy)

    except JSONDecodeError as error:
        print(f"Неправильный формат файла {path_fav_employers}, {error}")


def count_companies(dbmanager: DBManager) -> None:
    answer = dbmanager.get_companies_and_vacancies_count()
    if answer:
        print("Количество вакансий для каждого работодателя: ")
        table = PrettyTable()
        table.field_names = ["Работодатель",  "Кооличество вакансий"]
        for row in answer:
            table.add_row(row)
        print(table)


def avg_salary(dbmanager: DBManager) -> None:
    answer = dbmanager.get_avg_salary()
    if answer:
        print("Средняя зарплата: ", answer)

def all_vacancies(dbmanager: DBManager) -> None:
    answer = dbmanager.get_all_vacancies()
    if answer:
        names = ["Работодатель",  "Вакансия", "Зарплата от", "Зарплата до", "Вал.", "Ссылка"]
        print(names)
        for row in answer:
            print(row)

def salary_gr_avarage(dbmanager: DBManager) -> None:
    answer = dbmanager.get_vacancies_with_higher_salary()
    if answer:
        # names = ["Работодатель",  "Вакансия", "Зарплата от", "Зарплата до", "Вал.", "Ссылка"]
        # print(names)
        for row in answer:
            print(row)

def vacancy_keyword(dbmanager: DBManager, keyword: str) -> None:
    answer = dbmanager.get_vacancies_with_keyword(keyword)
    if answer:
        for row in answer:
            print(row)

def menu(dbmanager: DBManager) -> None:
    clrscr()
    print("Выберите нужное действие:")
    print("1 - Посчитать вакансии у каждого работодателя")
    print("2 - Вывести среднюю зарплату")
    print("3 - Вывести список всех вакансий")
    print("4 - Вывести список всех вакансий, у которых зарплата выше средней")
    print("5 - Вывести список всех вакансий, в названии которых содержится ключевое слово")
    print("6 - Выход.")
    # (Exit - ctrl + Z)
    try:
        result = input()
        match result:
            case ("1"):
                try:
                    count_companies(dbmanager)
                except Exception as error:
                    print(error)
                input("Для продолжения нажмите любую клавишу.")
            case ("2"):
                avg_salary(dbmanager)
                input("Для продолжения нажмите любую клавишу.")
            case ("3"):
                all_vacancies(dbmanager)
                input("Для продолжения нажмите любую клавишу.")
            case ("4"):
                salary_gr_avarage(dbmanager)
                input("Для продолжения нажмите любую клавишу.")
            case ("5"):
                text = input("Введите ключевое слово для поиска: ")
                vacancy_keyword(dbmanager, text)
                input("Для продолжения нажмите любую клавишу.")
            case ("6"):
                exit()
    except EOFError:
        exit()


def main():
    try:
        dbmanager = DBManager()
    except FileNotFoundError as error:
        print(error)

    while True:
        clrscr()
        print("------Парсер вакансий для работы с базой данных Postgresql------")
        print("Выберите нужное действие:")
        print("1 - Сделать запрос на сайт hh.ru по списку работодателей и сохранить данные в базе данных")
        print("2 - Получить данные из базы данных")
        print("3 - Выход.")
        # (Exit - ctrl + Z)
        try:
            result = input()
            match result:
                case ("1"):
                    try:
                        create_tables(dbmanager)
                        fill_tables(dbmanager)
                    except Exception as error:
                        print(error)
                case ("2"):
                    menu(dbmanager)
                case ("3"):
                    exit()

        except EOFError:
            exit()


if __name__ == "__main__":
    main()