class Vacancy_sql:
    """Class Vacancy_sql for representing a vacancy object.
    Atributes:
    - id:int -  id of the vacancy on the source site,
    - title:str - job title,
    - salary_from: float - minimum salary level,
    - salary_to: float - maximum salary level,
    - url:str - vacancy address,
    - description:str -  job description,
    - firm_name:str -name of the employer organization,
    - service:str- the name of the site from which vacancies were received.
    Takes the values HH and SJ.
      """
    __slots__ = ('id', 'vacancy_employer_id', 'name', 'area', 'salary_from', 'salary_to', 'salary',
        'description', 'salary_currency', 'salary_gross', 'published_at', 'url',
        'firm_name', 'service', 'requirement', 'responsibility', 'contacts',
        'experience', 'employment')

    def __init__(self, id: str = "", vacancy_employer_id = "", name: str = "",
        area: str  = "",
        salary_from: float = 0.0,
        salary_to: float = 0.0,
        salary_currency: str = "",
        salary_gross: bool = False,
        salary: float = 0.0,
        published_at = "01.01.0001",
        url: str = "",
        requirement: str = "",
        contacts: str = "",
        experience: str = "",
        employment: str = "",
        responsibility: str = ""
        ):
        self.id = id
        self.vacancy_employer_id = vacancy_employer_id
        self.name = name
        self.area = area
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary = salary
        self.salary_currency = salary_currency
        self.salary_gross = salary_gross
        self.published_at = published_at
        self.url = url
        self.requirement = requirement
        self.responsibility = responsibility
        self.contacts = contacts
        self.experience = experience
        self.employment = employment

    def __str__(self):
        return f'{self.service} id:{self.id}, {self.name}, {self.salary_from} - {self.salary_to} {self.salary_currency}'

    def __repr__(self):
        return f'{self.service} id:{self.id}, {self.name}, {self.salary_from} - {self.salary_to} {self.salary_currency}'
