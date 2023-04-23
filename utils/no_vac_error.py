class NoVacationError(Exception):
    """The NoVacationError class is used to handle an exception that occurs
    if no vacancies are returned in a request to a site with vacancies.

    Attributes:
    -message:str - error message

    Methods:
    -__init__ - initializing an instance of an object of class NoVacationError
    -__str__- returns a text to print with an error message
    """
    def __init__(self, message=""):
        if message:
            self.message = message
        else:
            self.message = None

    def __str__(self):
        """ returns the type of error and the message"""
        return "NoVacationError: " + str(self.message)
