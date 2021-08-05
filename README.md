# api_final

## Описание:

    REST API для Yatube. 
    Через этот интерфейс смогут работать мобильное приложение или чат-бот; через него же можно будет передавать данные в любое приложение или на фронтенд.

## Как запустить проект:

    Клонировать репозиторий и перейти в него в командной строке:

    ```
    git clone https://github.com/Viktor-Gostyaikin/api_final_yatube.git
    ```

    ```
    cd api_final_yatube
    ```

    Cоздать и активировать виртуальное окружение:

    ```
    python3 -m venv env
    ```

    ```
    source env/bin/activate
    ```

    ```
    python3 -m pip install --upgrade pip
    ```

    Установить зависимости из файла requirements.txt:

    ```
    pip install -r requirements.txt
    ```

    Выполнить миграции:

    ```
    python3 manage.py migrate
    ```

    Запустить проект:

    ```
    python3 manage.py runserver
    ```

## Примеры:

### Пример POST-запроса с токеном Антона Чехова: добавление нового поста.

    [POST] .../api/v1/posts/

        {
            "text": "Вечером собрались в редакции «Русской мысли», чтобы поговорить о народном театре. Проект Шехтеля всем нравится."
        }
     
__Пример ответа:__
        {
            "id": 14,
            "text": "Вечером собрались в редакции «Русской мысли», чтобы поговорить о народном театре. Проект Шехтеля всем нравится.",
            "author": "anton",
            "image": null,
            "group": 1,
            "pub_date": "2021-06-01T08:47:11.084589Z"
        } 

### Пример POST-запроса с токеном Антона Чехова: отправляем новый комментарий к посту с id=14.

    [POST] .../api/v1/posts/14/comments/
        {
            "text": "тест тест",
        } 

__Пример ответа:__
        {
            "id": 4,
            "author": "anton",
            "post": 14,
            "text": "тест тест",
            "created": "2021-06-01T10:14:51.388932Z"
        } 
### Пример GET-запроса с токеном Антона Чехова: получаем информацию о группе.

    [GET] .../api/v1/groups/2/

__Пример ответа:__
        {
            "id": 2,
            "title": "Математика",
            "slug": "math",
            "description": "Посты на тему математики"
        } 