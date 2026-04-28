from api.requests.base_requests_api import BaseApi
from data.data_api import BaseApiLocators
from typing import List, Union, Dict, Any
from api.requests.model import Entity
from api.requests.exceptions import EntityNotFoundError, InvalidJsonError, ApiRequestError,UnexpectedResponseError
import json


class ApiHelper(BaseApi):
    def __init__(self):
        super().__init__()
        self.locators = BaseApiLocators()

    def _check_status_code(self, response, expected_status: int) -> None:
        """Проверка статуса ответа."""
        if response.status_code != expected_status:
            raise ApiRequestError(
                f"Ошибка запроса. Статус: {response.status_code}, "
                f"Ответ: {response.text}"
            )

    def _parse_json_response(self, response) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Парсинг JSON-ответа."""
        try:
            data = response.json()
        except ValueError as e:
            raise InvalidJsonError(f"Ответ не является валидным JSON: {response.text}") from e
        return data

    def get_entity(self, entity_id: int) -> Entity:
        """Получение сущности по id"""
        response = self.request_get(self.locators.URL_get.format(entity_id))
        self._check_status_code(response, 200)
        data = self._parse_json_response(response)
        if not isinstance(data, dict):
            raise InvalidJsonError(f"Ожидался JSON объект, получен: {type(data).__name__}: {data}")
        return Entity(**data)

    def get_all_entities(self) -> List[Entity]:
        """Получение всех сущностей"""
        response = self.request_get(self.locators.URL_get_all)
        self._check_status_code(response, 200)
        data = self._parse_json_response(response)
        
        if isinstance(data, dict) and 'entity' in data:
            entities_list = data['entity']
        elif isinstance(data, list):
            entities_list = data
        else:
            raise UnexpectedResponseError(f"Неожиданная структура ответа: {type(data).__name__}: {data}")
        
        if not isinstance(entities_list, list):
            raise InvalidJsonError(f"Ожидался JSON массив, получен: {type(entities_list).__name__}: {entities_list}")  

        return [Entity(**item) for item in entities_list]

    def create_entity(self, entity_data: dict) -> Entity:
        print(self.locators.URL_create)
        print(json.dumps(entity_data))
        response = self.request_post(
            self.locators.URL_create,
            json=entity_data
        )

        self._check_status_code(response, 201)
        if not response.text:
            raise UnexpectedResponseError("Сервер вернул пустой ответ")

        try:
            entity_id = int(response.text.strip())
        except ValueError:
            try:
                data = response.json()
                if isinstance(data, dict):
                    return Entity(**data)
                else:
                    entity_id = int(data)
            except (ValueError, TypeError):
                raise UnexpectedResponseError(f"Неожиданный ответ от сервера: {response.text}")

        return self.get_entity(entity_id)

    def update_entity(self, entity_id: int, entity_data: dict) -> int:
        """Обновление сущности (возвращает статус код)"""
        response = self.request_patch(
            self.locators.URL_update.format(entity_id),
            json=entity_data
        )
        self._check_status_code(response, 204)
        return response.status_code

    def delete_entity(self, entity_id: int) -> int:
        """Удаление сущности (возвращает статус успеха)"""
        response = self.request_delete(self.locators.URL_delete.format(entity_id))
        return response.status_code