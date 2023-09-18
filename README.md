# Проект «Фудграм»
## Описание
[«Фудграм»](https://foodgram.host) это сайт на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд
## Установка и запуск проекта
*Клонируйте репозиторий:*

```
git clone git@github.com:PullZZZ/foodgram-project-react.git
```

*Перейдите в директорию infra и создайте файл .env,
можно скопировать представленный там пример .env.example*

```
cp .env.example .env
```
*Отредактируйте его в соответсвии со своими настройками*
*Для запуска введите команду*
```
docker compose up -d
```
*После успешного запуска контейнеров, выполните миграции*

```
docker compose exec backend python manage.py migrate
```
*Соберите и скопируйте статику backend-части проекта*

```
docker compose exec backend python manage.py collectstatic
docker compose exec backend cp -r /app/foodgram/collected_static/. /backend_static/static/
```
*Создайте superuser*

```
docker compose exec backend python manage.py createsuperuser
```
Проект будет доступен по адресу (http://localhost)

## Заполнение базы данных
Для импорта в базу даннтых об ингредиентах и тегах можно использовать заранее подготовленные данные в файлах csv и json, примеры файлов находятся в директории data
```
docker compose exec backend python manage.py load_data
```
информация о командах импорта
```
docker compose exec backend python manage.py load_data --help
```
Импорт так-же возможен из панели администратора

## Докуметация

После запуска проекта по адресу http://localhost/api/docs/ будет доступна документация для api проекта
## Технологии проекта
В проекте использованны
- Python
- Django
- Django Rest Framework
- Docker
- Nginx
- PostgreSQL
## Автор
[Данила Савицкий ![GitHub](https://img.shields.io/badge/-GitHub-464646??style=flat-square&logo=GitHub)](https://github.com/PullZZZ)
Проект доступен по адресу: https://foodgram.host
