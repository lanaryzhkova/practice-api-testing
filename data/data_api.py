import os
from dotenv import load_dotenv

load_dotenv()

class BaseApiLocators():

    URL = os.getenv('BASE_URL')
    URL_create = f"{URL}/create"
    URL_delete = f"{URL}/delete/{{}}"
    URL_get = f"{URL}/get/{{}}"
    URL_get_all = f"{URL}/getAll"
    URL_update = f"{URL}/patch/{{}}"

