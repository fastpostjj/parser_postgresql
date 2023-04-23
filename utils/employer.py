class Employer():
    """Класс Employer для представления данных работодателя"""

    __slots__ = ('id', 'name', 'description', 'url', 'alternate_url', 'trusted')

    def __init__(
        self, id: str = "", name: str = "",
        description: str = "",
        url: str = "",
        alternate_url: str = "", trusted: bool = True
        ) -> None:

        self.id = id
        self.name = name
        self.description = description
        self.url = url
        self.alternate_url = alternate_url
        self.trusted = trusted

    def __repr__(self):
        return f'Employer(id={self.id}, name={self.name},url={self.url}, alternate_url={self.alternate_url}, trusted={self.trusted})'
