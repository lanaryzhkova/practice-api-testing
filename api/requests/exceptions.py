class ApiRequestError(Exception):
    """Базовое исключение для ошибок API-запросов."""
    pass

class EntityNotFoundError(ApiRequestError):
    """Исключение для случаев, когда сущность не найдена."""
    pass

class InvalidJsonError(ApiRequestError):
    """Исключение для невалидного JSON-ответа."""
    pass

class UnexpectedResponseError(ApiRequestError):
    """Исключение для неожиданной структуры ответа."""
    pass