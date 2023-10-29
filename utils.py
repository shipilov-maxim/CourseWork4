from abc import abstractmethod, ABC
import requests
from datetime import datetime


class APIVacancy(ABC):

    @abstractmethod
    def get_vacancies(self, vacancy, salary):
        pass

    @abstractmethod
    def format_data(self, data):
        pass


class HeadHunterAPI(APIVacancy):
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, vacancy, salary):
        headers = {'User-Agent': 'skam3840@gmail.com'}
        parameters = {'text': vacancy,
                      'only_with_salary': True,
                      'salary': salary,
                      'per_page': 100}

        response = requests.get(self.url, headers=headers, params=parameters).json()
        return response

    def format_data(self, data):
        vacancy_dict = {}
        for vacancy in data['items']:
            vacancy_id = vacancy['id']
            if vacancy['salary']['from'] is not None:
                salary_from = f"от {vacancy['salary']['from']} "
            else:
                salary_from = ""
            if vacancy['salary']['to'] is not None:
                salary_to = f"до {vacancy['salary']['to']} "
            else:
                salary_to = ""
            requirement = vacancy['snippet']['requirement']
            responsibility = vacancy['snippet']['responsibility']
            published = vacancy['published_at']
            date_published = datetime.strptime(published, "%Y-%m-%dT%H:%M:%S%z")
            vacancy_dict[vacancy_id] = {'url': f"https://hh.ru/vacancy/{vacancy_id}",
                                        'name': vacancy['name'],
                                        'salary': f"{salary_from}{salary_to}{vacancy['salary']['currency']}",
                                        'requirement': requirement,
                                        'responsibility': responsibility,
                                        'date_published': date_published.strftime("%d.%m.%Y")}

        return vacancy_dict


class SuperJobAPI:
    pass

    def get_vacancies(self, vacancy):
        pass

    def format_data(self):
        pass


class Vacancy:
    pass


class JSONSaver:
    def add_vacancy(self):
        pass

    def get_vacancies_by_salary(self):
        pass

    def delete_vacancy(self):
        pass


hh_api = HeadHunterAPI()
hh_vacancies = hh_api.get_vacancies("Python", 10000)
print(hh_api.format_data(hh_vacancies))
