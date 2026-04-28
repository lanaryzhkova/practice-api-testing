# API Testing Project

## О проекте

Проект содержит автоматизированные API тесты для проверки CRUD операций с сущностями:

- создание сущности  
- получение по ID  
- получение списка  
- обновление  
- удаление  

---

## Запуск локально

### 1. Установка зависимостей

pip install -r requirements.txt

---

### 2. Запуск тестового сервиса


git clone https://github.com/sun6r0/test-service.git

cd test-service
docker compose up -d --build

---

### 3. Запуск тестов


pytest tests/ -v --alluredir=allure-results

---

### 4. Генерация Allure отчёта


allure generate allure-results -o allure-report --clean
allure open allure-report

---

Реализованы позитивные сценарии:

- ✔ создание сущности  
- ✔ получение по ID  
- ✔ получение списка  
- ✔ обновление  
- ✔ удаление  
