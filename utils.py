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
        vacancy_list = []
        for vacancy in data['items']:
            date_published = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
            vacancy_dict = {'url': f"https://hh.ru/vacancy/{vacancy['id']}",
                            'name': vacancy['name'],
                            'salary': [vacancy['salary']['from'], vacancy['salary']['to'],
                                       vacancy['salary']['currency']],
                            'requirement': vacancy['snippet']['requirement'],
                            'responsibility': vacancy['snippet']['responsibility'],
                            'date_published': date_published.strftime("%d.%m.%Y")}
            vacancy_list.append(vacancy_dict)
        return vacancy_list


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
        vacancy_list = []
        for vacancy in data['objects']:
            try:
                responsibility = vacancy['client']['description']
            except KeyError:
                responsibility = ''
            vacancy_dict = {'url': vacancy['link'],
                            'name': vacancy['profession'],
                            'salary': [vacancy['payment_from'],
                                       vacancy['payment_to'], vacancy['currency']],
                            'requirement': vacancy['candidat'],
                            'responsibility': responsibility,
                            'date_published': ''}
            vacancy_list.append(vacancy_dict)
        return vacancy_list


class Vacancy:
    def __init__(self, url, name, salary, requirement, responsibility, date_published):
        self.url = url
        self.name = name
        self.salary = salary
        self.requirement = requirement
        self.responsibility = responsibility
        self.date_published = date_published

        self.salary_max = self.salary_max()

    def __repr__(self):
        return (f"{self.name}\n{self.url}\n{self.salary_max} {self.salary[2]}\n{self.requirement}\n"
                f"{self.responsibility}\nДата публикации: {self.date_published}")

    def salary_max(self):
        if self.salary[1] is None and self.salary[0] is None:
            return 0
        elif self.salary[1] is None :
            return self.salary[0]
        elif self.salary[0] is None:
            return self.salary[1]
        elif self.salary[0] > self.salary[1]:
            return self.salary[0]
        elif self.salary[0] <= self.salary[1]:
            return self.salary[1]


class JSONSaver:
    @staticmethod
    def save_file(data):
        with open('vacancies.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def add_vacancy(vacancy):
        with open('vacancies.json', "r+", encoding='utf-8') as f:
            data = json.load(f)
            [data.append(v) for v in vacancy]
        with open('vacancies.json', "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def load_from_file():
        vacancies = []
        with open('vacancies.json', encoding='utf-8') as f:
            text = f.read()
        text = json.loads(text)
        for item in text:
            vacancies.append(Vacancy(item['url'],
                                     item['name'],
                                     item['salary'],
                                     item['requirement'],
                                     item['responsibility'],
                                     item['date_published']))
        return vacancies


def filter_vacancies(list_, filter_word):
    d = []
    [d.append(v) for v in list_ if filter_word in repr(v)]
    return d


def sort_vacancies(list_v):
    sorted_data = sorted(list_v, key=lambda x: x.salary_max, reverse=True)
    return sorted_data


def get_top_vacancies(list_v, top_n):
    return [print(v) for v in list_v[:top_n]]

