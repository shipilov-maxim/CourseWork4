from utils import *


# Функция для взаимодействия с пользователем
def user_interaction():
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI()

    platforms = ["HeadHunter", "SuperJob"]
    print(f"Платформы для поиска:")
    [print(p) for p in platforms]
    search_query = input(f"Введите поисковый запрос: ")

    # Получение вакансий с разных платформ
    hh_vacancies = hh_api.get_vacancies(search_query)
    superjob_vacancies = superjob_api.get_vacancies(search_query)
    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    except ValueError:
        top_n = 1
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ")

    js = JSONSaver

    format_hh = hh_api.format_data(hh_vacancies)
    js.save_file(format_hh)
    format_sj = superjob_api.format_data(superjob_vacancies)
    js.add_vacancy(format_sj)

    list_v = js.load_from_file()

    filtered_vacancies = filter_vacancies(list_v, filter_words)

    if not filtered_vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    sorted_vacancies = sort_vacancies(filtered_vacancies)

    get_top_vacancies(sorted_vacancies, top_n)


if __name__ == "__main__":
    user_interaction()
