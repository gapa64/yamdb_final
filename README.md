# Квик старт

Проект **yamdb final** Реализует CI\CD модель для проекта api_yamdb, развернутого в контейнерах Docker.  
api_yamdb собирает отзывы пользователей на произведения

## Проверить
[api/v1](http://51.250.16.106/api/v1/)  
[admin](http://51.250.16.106/admin)  
[redoc](http://51.250.16.106/redoc)  

```bash
Публичный IPv4 адрес сервера: 51.250.16.106
```
## Заметь
Миграции и сбор статики реализованы через Docker а не через Compose из-за неисправленной бага Compose [8201](https://github.com/docker/compose/issues/8201)

## Заупстить

```bash
git clone https://github.com/gapa64/yamdb_final
docker-compose -f yamdb_final/infra/docker-compose.yaml up
```

### Шаблон env
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### Некоторые полезные команды
```bash
docker-compose exec web python manage.py migrate 
Применить миграции

docker-compose exec web python manage.py createsuperuser 
Создать супер пользователя Django

docker-compose exec web python manage.py collectstatic --no-input 
Cобрать статику

docker-compose exec web python manage.py loaddata fixtures.json
Загрузить тестовые данные
```

### Полезные линки
```bash
Docker image проекта api_yamdb  gaps64/api_yamdb:v2.4
```

## Автор
- [Sergey K](https://github.com/gapa64)

![yamdb workflow](https://github.com/gapa64/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
