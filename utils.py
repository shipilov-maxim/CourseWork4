from abc import abstractmethod, ABC
from datetime import datetime
import os
import requests
import json


class API(ABC):

    @abstractmethod
    def get_vacancies(self, vacancy):
        pass

    @abstractmethod
    def format_data(self, data):
        pass


class HeadHunterAPI(API):
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, vacancy):
        headers = {'User-Agent': 'skam3840@gmail.com'}
        parameters = {'text': vacancy,
                      'only_with_salary': True,
                      'per_page': 100}
        response = requests.get(self.url, headers=headers, params=parameters).json()
        return response

    def format_data(self, data):
        vacancy_dict = {}
        for vacancy in data['items']:
            date_published = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
            vacancy_dict[vacancy['id']] = {'url': f"https://hh.ru/vacancy/{vacancy['id']}",
                                           'name': vacancy['name'],
                                           'salary': [vacancy['salary']['from'], vacancy['salary']['to'],
                                                      vacancy['salary']['currency']],
                                           'requirement': vacancy['snippet']['requirement'],
                                           'responsibility': vacancy['snippet']['responsibility'],
                                           'date_published': date_published.strftime("%d.%m.%Y")}
        return vacancy_dict


class SuperJobAPI(API):
    def __init__(self):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'

    def get_vacancies(self, vacancy):
        api_key: str = os.getenv('SUPERJOB_API_KEY')
        headers = {f'Host': 'api.superjob.ru',
                   'X-Api-App-Id': api_key,
                   'Authorization': 'Bearer r.000000010000001.example.access_token',
                   'Content-Type': 'application/x-www-form-urlencoded'}
        parameters = {'keyword': vacancy,
                      'payment_defined': 1,
                      'payment_value': 1,
                      'per_page': 100
                      }
        response = requests.get(self.url, headers=headers, params=parameters).json()
        return response

    def format_data(self, data):
        vacancy_dict = {}
        for vacancy in data['objects']:
            try:
                responsibility = vacancy['client']['description']
            except KeyError:
                responsibility = ''
            vacancy_dict[vacancy['id']] = {'url': vacancy['link'],
                                           'name': vacancy['profession'],
                                           'salary': [vacancy['payment_from'],
                                                      vacancy['payment_to'], vacancy['currency']],
                                           'requirement': vacancy['candidat'],
                                           'responsibility': responsibility,
                                           'date_published': ''}
        return vacancy_dict


class Vacancy:
    def __init__(self, url, name, salary, requirement, responsibility, date_published):
        self.url = url
        self.name = name
        self.salary = salary
        self.requirement = requirement
        self.responsibility = responsibility
        self.date_published = date_published

    def __repr__(self):
        return f"""{self.name}
{self.url}
{self.salary}
{self.requirement}
{self.responsibility}
Дата публикации: {self.date_published}"""


class JSONSaver:
    @staticmethod
    def save_file(data):
        with open('vacancies.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def add_vacancy(vacancy):
        with open('vacancies.json', "r+", encoding='utf-8') as f:
            data = json.load(f)
            data.append(vacancy)
        with open('vacancies.json', "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def load_from_file():
        vacancies = []
        with open('vacancies.json', encoding='utf-8') as f:
            text = f.read()
        text = json.loads(text)
        for key, value in text.items():
            vacancies.append(Vacancy(value['url'],
                                     value['name'],
                                     value['salary'],
                                     value['requirement'],
                                     value['responsibility'],
                                     value['date_published']))
        return vacancies

    def get_vacancies_by_salary(self):
        pass

    def delete_vacancy(self):
        pass


hh_api = SuperJobAPI()
js = JSONSaver
hh_vacancies = hh_api.get_vacancies("Python")
fos = hh_api.format_data(hh_vacancies)
# print(fos)
js.save_file(fos)
print(js.load_from_file())


