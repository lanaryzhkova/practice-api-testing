from pydantic import BaseModel, Field


class EntityAddition(BaseModel):
    """Модель дополнения к сущности"""
    additional_info: str = Field(..., description='Дополнительное сведение о сущности')
    additional_number: int = Field(..., description='Дополнительное число для сущности')

class Entity(BaseModel):
    """Модель сущности"""
    id: int = Field(..., description='Идентификатор сущности')
    title: str = Field(..., description='Название сущности')
    verified: bool = Field(..., description='Описание сущности')
    important_numbers: list = Field(..., description='important_numbers сущности')
    addition: EntityAddition = Field(..., description='Дополнение к сущности')

class EntityList(BaseModel):
    """Модель списка сущностей"""
    entities: list[Entity] = Field(..., description='Список сущностей')
