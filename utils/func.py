from utils.vacancy_sql import Vacancy_sql
from utils.employer import Employer


def get_employer_from_json(data: dict) -> Employer:
    """
    function gets data from json (only one dictionary) and creates
    new instances of classes Employer
    """
    new_employer = Employer()
    if isinstance(data, dict):
        if "id" in data:
            new_employer.id = data["id"]
            if ("name" in data)\
                and data["name"]:
                new_employer.name = data["name"]
            if "description" in data\
                and data["description"]:
                new_employer.description = data["description"]
            if "url" in data:
                new_employer.url = data["url"]
            if "alternate_url" in data:
                new_employer.alternate_url = data["alternate_url"]
            if "trusted" in data:
                new_employer.trusted = data["trusted"]

        return new_employer
    else:
        raise KeyError("Неправильный тип данных (ожидается словарь)")


def get_vacancy_from_json(vacancy: dict) -> Vacancy_sql:
    """
    function gets data from json (only one dictionary) and creates new instances
     of classes Vacancy_sql
    """
    new_vacancy = Vacancy_sql()
    if isinstance(vacancy, dict):
        if "id" in vacancy:
            # no new instance Vacancy without id
            new_vacancy.id = vacancy["id"]
            new_vacancy.vacancy_employer_id = ""
            new_vacancy.name = ""
            new_vacancy.salary_from = 0.0
            new_vacancy.salary_to = 0.0
            new_vacancy.url = ""
            new_vacancy.description = ""
            new_vacancy.salary_currency = ""
            new_vacancy.firm_name = ""
            new_vacancy.service = ""

            if "name" in vacancy:
                new_vacancy.name = vacancy["name"]
                if vacancy["salary"] and ("salary" in vacancy) and\
                    ("from" in vacancy["salary"])\
                    and vacancy["salary"]["from"]:
                    new_vacancy.salary_from = float(vacancy["salary"]["from"])
                if vacancy["salary"] and ("salary" in vacancy) and\
                    ("to" in vacancy["salary"])\
                    and vacancy["salary"]["to"]:
                    new_vacancy.salary_to = float(vacancy["salary"]["to"])
                if vacancy["salary"] and ("salary" in vacancy) and\
                    ("currency" in vacancy["salary"]):
                    new_vacancy.salary_currency = vacancy["salary"]["currency"]
                if vacancy["salary"] and ("salary" in vacancy) and\
                    ("gross" in vacancy["salary"]):
                    new_vacancy.salary_gross = vacancy["salary"]["gross"]

                if "published_at" in vacancy:
                    new_vacancy.published_at = vacancy["published_at"]

                if "snippet" in vacancy:
                    if "requirement" in vacancy["snippet"]:
                        new_vacancy.requirement = vacancy["snippet"]["requirement"]
                    if "responsibility" in vacancy["snippet"]:
                        new_vacancy.responsibility = vacancy["snippet"]["responsibility"]
                if "url" in vacancy:
                    new_vacancy.url = vacancy["url"]
                if ("area" in vacancy) and\
                    ("name" in vacancy["area"])\
                    and vacancy["area"]["name"]:
                    new_vacancy.area = vacancy["area"]["name"]
                if "contacts" in vacancy:
                    new_vacancy.contacts = vacancy["contacts"]
                if ("experience" in vacancy) and\
                    ("name" in vacancy["experience"])\
                    and vacancy["experience"]["name"]:
                    new_vacancy.experience = vacancy["experience"]["name"]
                if ("employment" in vacancy) and\
                    ("name" in vacancy["employment"])\
                    and vacancy["employment"]["name"]:
                    new_vacancy.employment = vacancy["employment"]["name"]


                if ("employer" in vacancy):
                    if "id" in vacancy["employer"]:
                        # new_employer.id = vacancy["employer"]["id"]
                        new_vacancy.vacancy_employer_id = vacancy["employer"]["id"]
                        """
                        if ("name" in vacancy["employer"])\
                            and vacancy["employer"]["name"]:
                            new_employer.name = vacancy["employer"]["name"]
                        if "url" in vacancy["employer"]:
                            new_employer.url = vacancy["employer"]["url"]
                        if "alternate_url" in vacancy["employer"]:
                            new_employer.alternate_url = vacancy["employer"]["alternate_url"]
                        if "trusted" in vacancy["employer"]:
                            new_employer.trusted = vacancy["employer"]["trusted"]
                            """

            if new_vacancy.salary_to != 0.0:
                new_vacancy.salary = new_vacancy.salary_to
            else:
                new_vacancy.salary = new_vacancy.salary_from

        return new_vacancy
    else:
        raise KeyError("Неправильный тип данных (ожидается словарь)")
