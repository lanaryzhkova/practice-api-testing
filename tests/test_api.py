import pytest
import allure
from api.requests.model import Entity
from helpers.api_helper import ApiHelper
from helpers.utils import randomString, randomIntList, randomInt, randomBoolean


@pytest.fixture
def api_helper() -> ApiHelper:
    """Создает объект ApiHelper для выполнения запросов к API"""
    helper = ApiHelper()
    return helper


@pytest.fixture
def create_entity(api_helper: ApiHelper):
    """Фикстура создаёт сущность и возвращает её"""
    CREATE_ENTITY_DATA = {
    "title": randomString(),
    "verified": randomBoolean(),
    "important_numbers": randomIntList(),
    "addition": {
        "additional_info": randomString(),
        "additional_number": randomInt()
    }
}
    with allure.step("Предусловие: создание сущности"):
        entity = api_helper.create_entity(CREATE_ENTITY_DATA)

    yield entity

    with allure.step("Постусловие: удаление сущности"):
        api_helper.delete_entity(entity.id)


@allure.suite("API тесты для сущностей")
@allure.feature("Позитивные сценарии")
class TestEntityApiPositive:
    """Тесты для сущностей"""
    @allure.title("Создание сущности")
    @allure.description("Проверка успешного создания сущности с валидными данными")
    def test_create_entity(self, api_helper: ApiHelper):
        """Функция тестирования создания сущности"""
        with allure.step("Отправка запроса на создание сущности"):
            entity = api_helper.create_entity
        
        with allure.step("Проверка ответа"):
            assert isinstance(entity, Entity)
            assert entity.title == CREATE_ENTITY_DATA["title"]
            assert entity.verified == CREATE_ENTITY_DATA["verified"]
            assert entity.important_numbers == CREATE_ENTITY_DATA["important_numbers"]
            assert entity.addition.additional_info == CREATE_ENTITY_DATA["addition"]["additional_info"]
            assert entity.addition.additional_number == CREATE_ENTITY_DATA["addition"]["additional_number"]
            assert entity.id > 0

    @allure.title("Получение сущности по ID")
    @allure.description("Проверка успешного получения сущности по её идентификатору")
    def test_get_entity_by_id(self, api_helper: ApiHelper, create_entity: Entity):
        """Функция тестирования получения сущности по его идентификатору"""
        entity_id = create_entity.id
        
        with allure.step(f"Запрос сущности с ID {entity_id}"):
            fetched_entity = api_helper.get_entity(entity_id)
        
        with allure.step("Проверка соответствия данных"):
            assert fetched_entity.id == entity_id
            assert fetched_entity.title == create_entity.title
            assert fetched_entity.verified == create_entity.verified
            assert fetched_entity.important_numbers == create_entity.important_numbers
            assert fetched_entity.addition.additional_info == create_entity.addition.additional_info
            assert fetched_entity.addition.additional_number == create_entity.addition.additional_number

    @allure.title("Получение всех сущностей")
    @allure.description("Проверка успешного получения списка всех сущностей")
    def test_get_all_entities(self, api_helper: ApiHelper, create_entity: Entity):
        """Функция тестирования получения списка всех сущностей"""
        with allure.step("Запрос всех сущностей"):
            entities = api_helper.get_all_entities()
        
        with allure.step("Проверка, что список не пуст и содержит созданную сущность"):
            assert isinstance(entities, list)
            assert len(entities) > 0
            ids = [e.id for e in entities]
            assert create_entity.id in ids

    @allure.title("Обновление сущности")
    @allure.description("Проверка успешного обновления сущности")
    def test_update_entity(self, api_helper: ApiHelper, create_entity: Entity):
        """Функция тестирования обновления сущности"""
        entity_id = create_entity.id
        update_data = {
            "title": "Обновлённый заголовок",
            "verified": randomBoolean(),
            "important_numbers": randomIntList(),
            "addition": {
                "additional_info": randomString(),
                "additional_number": randomInt()
            }
        }
        
        with allure.step(f"Отправка запроса на обновление сущности с ID {entity_id}"):
            status_code = api_helper.update_entity(entity_id, update_data)
        
        with allure.step("Проверка статус-кода (204 No Content)"):
            assert status_code == 204
        
        with allure.step("Получение обновлённой сущности для проверки изменений"):
            updated_entity = api_helper.get_entity(entity_id)
        
        with allure.step("Проверка обновлённых полей"):
            assert updated_entity.title == update_data["title"]
            assert updated_entity.verified == update_data["verified"]
            assert updated_entity.important_numbers == update_data["important_numbers"]
            assert updated_entity.addition.additional_info == update_data["addition"]["additional_info"]
            assert updated_entity.addition.additional_number == update_data["addition"]["additional_number"]

    @allure.title("Удаление сущности")
    @allure.description("Проверка успешного удаления сущности")
    def test_delete_entity(self, api_helper: ApiHelper):
        """Функция тестирования удаления сущности"""

        CREATE_ENTITY_DATA = {
            "title": randomString(),
            "verified": True,
            "important_numbers": randomIntList(),
            "addition": {
                "additional_info": randomString(),
                "additional_number": randomInt()
            }
        }
        
        entity = api_helper.create_entity(CREATE_ENTITY_DATA)
        entity_id = entity.id
        
        with allure.step(f"Удаление сущности с ID {entity_id}"):
            status_code = api_helper.delete_entity(entity_id)
        
        with allure.step("Проверка статус-кода (204 No Content)"):
            assert status_code == 204
        
        with allure.step("Попытка получить удалённую сущность (должна вернуть ошибку)"):
            try:
                api_helper.get_entity(entity_id)
                pytest.fail(f"Сущность с ID {entity_id} всё ещё существует после удаления")
            except Exception as e:
                allure.attach(str(e), name="Ошибка при запросе удалённой сущности", attachment_type=allure.attachment_type.TEXT)