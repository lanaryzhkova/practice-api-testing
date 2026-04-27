import requests
from requests import Response
from typing import Optional, Dict, Any


class BaseApi:
    """Базовый класс для API"""
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.body = None

    def request_get(self,
                    url: str,
                    *,
                    data: Optional[Dict[str, Any]] = None,
                    json: Optional[Dict[str, Any]] = None,
                    **kwargs: Any) -> Response:
        """Выполняет GET запрос"""
        return requests.get(url, headers=self.headers, **kwargs)
    
    def request_post(self,
                     url: str,
                     *,
                     data=None,
                     json=None,
                     **kwargs):
        """Выполняет POST запрос"""
        return requests.post(
            url,
            headers=self.headers,
            data=data,
            json=json,
            **kwargs
        )
    
    def request_patch(self,
                      url: str,
                      *,
                      data: Optional[Dict[str, Any]] = None,
                      json: Optional[Dict[str, Any]] = None,
                      **kwargs: Any) -> Response:
        """Выполняет PATCH запрос"""
        return requests.patch(url, headers=self.headers, data=data, json=json, **kwargs)
    
    def request_delete(self,
                       url: str,
                       *,
                       data: Optional[Dict[str, Any]] = None,
                       json: Optional[Dict[str, Any]] = None,
                      **kwargs: Any) -> Response:
        """Выполняет DELETE запрос"""
        return requests.delete(url, headers=self.headers, **kwargs)
    
