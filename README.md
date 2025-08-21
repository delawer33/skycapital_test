# Менедер задач (FastAPI, pytest)

## Запуск сервера

Копируем репозиторий и переходим в него
```bash
git clone https://github.com/delawer33/skycapital_test
```
```
cd skycapital_test
```


Для удобства и быстроты насторйки проекта я решил включить в репозиторий папку `alembic` с готовыми настройками и миграциями.

Далее приводятся инструкции для запуска сервера с помощью `docker` и локально на машине.

### Docker

1. В корневой директории создаем файл `.env` по примеру `.env.example` (можно просто скопировать содержимое)

2. Запускаем docker-compose
```
sudo docker compose up --build
```

3. Применяем миграции
```
alembic upgrade head
```

### Локально на машине
1. В `app/сonfig` создаем файл `.env` по примеру в файле `.env_example` (можно просто скопировать его содержимое в файл `.env`). В нем нужно будет указать url к БД.

2. Создаем виртуальное окружение (желательно python версии 3.12), активируем его, устанавливаем зависимости

```
python3 -m venv .venv
```
```
source .venv/bin/activate
```
```
pip install -r requirements.txt
```

3. Запускаем `postgres`. Если хотите запускать через Docker, то используйте команду
```
sudo docker compose up postgres --build
```

4. Применяем миграции
```
alembic upgrade head
```

5. Запускаем сервер 

```
python3 -m app.main
```

Swagger-документация на `localhost:8000/docs`

## Тесты
Тесты находятся в папке `tests`.
Для запуска тестов выполните команду
```
pytest
```
