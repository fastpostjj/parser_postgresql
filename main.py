import click
import json
from json import JSONDecodeError
from prettytable import PrettyTable
from utils.dbmanager import DBManager
from config import path_fav_employers, filename
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

    try:
        # Читаем список работодаттелей из файла
        with open(path_fav_employers, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError as error:
        print(f"Файл {path_fav_employers} не найден", error)
        input("Для продолжения нажмите любую клавишу.")
        return

    # Очищаем базу данных
    create_tables(dbmanager)

    # Читаем данные из файла работодателей
    try:
        list_data = json.loads(text)
    except JSONDecodeError as error:
        print(f"Неправильный формат файла {path_fav_employers}, {error}")
        input("Для продолжения нажмите любую клавишу.")
        return

    # Заполняем базу данных данными
    # Сначала заполняем таблицу employers
    for item in list_data:
        employer_dict = hh.get_request_employers(item["id"])
        employer = get_employer_from_json(employer_dict)
        try:
            dbmanager.insert_employer(employer)
        except Exception as error:
            print(error)
            input("Для продолжения нажмите любую клавишу.")
            return

        # Для каждого работодателя выбираем все вакансии
        # и заполняем таблицу vacancies
        list_vacancies = hh.get_request_employers_vacancies(item["id"])
        for vacancy_dict in list_vacancies:
            vacancy = get_vacancy_from_json(vacancy_dict)
            try:
                dbmanager.insert_vacancies(vacancy)
            except Exception as error:
                print(error)
                input("Для продолжения нажмите любую клавишу.")
                return


def count_companies(dbmanager: DBManager) -> None:
    answer = dbmanager.get_companies_and_vacancies_count()
    if answer:
        print("Количество вакансий для каждого работодателя: ")
        table = PrettyTable()
        table.field_names = ["Работодатель",  "Количество вакансий"]
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
    print("6 - Возврат в главное меню.")
    try:
        result = input()
        match result:
            case ("1"):
                try:
                    count_companies(dbmanager)
                    input("Для продолжения нажмите любую клавишу.")
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
                return
    except EOFError:
        exit()


def main():
    try:
        dbmanager = DBManager()
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
                            fill_tables(dbmanager)
                        except Exception as error:
                            print(error)
                            input("Для продолжения нажмите любую клавишу.")
                    case ("2"):
                        menu(dbmanager)
                    case ("3"):
                        exit()

            except EOFError:
                exit()
    except FileNotFoundError as error:
        print("Ошибка чтения файла database.ini, ", error)
        exit()
    except KeyError:
        print("Неправильно заданы параметры подключения к базе данных в файле", filename)


if __name__ == "__main__":
    main()