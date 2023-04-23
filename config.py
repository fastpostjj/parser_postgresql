import os
from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise FileNotFoundError(
            'Section {0} is not found in the {1} file.'.format(
                section,
                filename
                ))
    return db


path_fav_employers = os.sep.join(["data", "favorits_ employers.json"])

super_job_key = os.getenv("SUPER_JOB_KEY")
keyword = "Python"
file_path = os.sep.join(["results", "vacations.json"])
file_path_emp = os.sep.join(["results", "vacations.json"])

