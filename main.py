import requests
from requests import Response

from DataClass import GetUrlVacancy, DetailVacancyResponse



class HeadHunterPars:
    url = 'https://api.hh.ru/vacancies/'
    dict_vacancy = {}

    def __init__(self, params: dict):
        self._params = params

    def set_params(self,text: str, area: int, page: int, per_page: int):
        self._params = {
    'text': text,  # Текст фильтра. В имени должно быть слово "Аналитик"
    'area': area,  # Поиск ощуществляется по вакансиям города Москва
    'page': page,  # Индекс страницы поиска на HH
    'per_page': per_page, # Кол-во вакансий на 1 странице
}
        return self._params

    def netx_page(self,page: int):
        page_next = int(self._params['page']) + page
        self._params['page'] = page_next
        return self._params


    def response(self,url: str, params: dict)-> Response:
        links = requests.get(url=url, params=params)
        return links


    def get_items(self)-> GetUrlVacancy:
        links = requests.get(url=self.url, params=self._params)
        return GetUrlVacancy(**links.json())

    def get_url_by_vacancy(self) -> list:
        return [vacancy.url for vacancy in self.get_items().items]

    def get_detail_vacancy(self) -> list[DetailVacancyResponse]:
        list = []
        for vacancy in self.get_url_by_vacancy():
            response = self.response(url=vacancy, params=self._params)
            result = DetailVacancyResponse(**response.json())
            self.dict_vacancy[result.alternate_url] = result
            list.append(result)
        return list








