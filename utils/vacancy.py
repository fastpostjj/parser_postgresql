class Vacancy:
    """Class Vacancy for representing a vacancy object.
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
    __slots__ = ('id', 'title', 'salary_from', 'salary_to', 'salary', 'url',
        'description', 'currency', 'firm_name', 'service')

    def __init__(self, id, title: str = "",
                salary_from: float = 0.0,
                salary_to: float = 0.0,
                salary: float = 0.0,
                url: str = "",
                description: str = "",\
                currency: str = "",
                firm_name: str = "",
                service: str = ""):
        self.id = id
        self.title = title
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary = salary
        self.currency = currency
        self.url = url
        self.description = description
        self.firm_name = firm_name
        self.service = service

    def __str__(self):
        return f'{self.service} id:{self.id}, {self.title}, {self.salary_from} - {self.salary_to} {self.currency}, {self.firm_name}'

    def __repr__(self):
        return f'{self.service} id:{self.id}, {self.title}, {self.salary_from} - {self.salary_to} {self.currency}, {self.firm_name}'
