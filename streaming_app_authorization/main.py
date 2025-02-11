from fastapi import FastAPI, Query, Path, Body, HTTPException, Response, Depends, Request, status, Header
from starlette.responses import HTMLResponse, JSONResponse

from streaming_app_authorization.schemas import *
from streaming_app_authorization.services import *
from streaming_app_authorization.database.db import *
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse

app = FastAPI()


# Асинхронная функция добавление пользователя в БД
@app.post("/registration")
async def registration(creds_registration: RegistrationUserSchema):
    # Подготавливаем данные для сохранения
    user_data = creds_registration.dict()

    # Сохраняем пользователя в БД
    query = await async_collection.insert_one(user_data)

    # Проверка, добавился ли документ в БД, если нет - кидаем ошибку
    if query.inserted_id:
        return {"message": "user created", "id": str(query.inserted_id)}
        # return RedirectResponse(url="/login",  status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    raise HTTPException(status_code=500, detail="Failed to create item")


# Авторизация
@app.post('/login')
async def login(creds_login: LoginUserSchema, response: Response):
    # Ищем пользователя по 'username'
    query = await async_collection.find_one({"username": creds_login.username})
    if query:
        # Генерируем токен доступа
        # Токен хранит id юзера в uid
        access_token = create_access_token(uid=str(query["_id"]))

        # Cоздаю куки и записываю в них access_token
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=access_token,
            httponly=True,
            secure=True,
            samesite='lax',
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)

        # Если всё в порядке, редиректим на домашнюю страницу
        # return {"message": "Login successful, cookie created!"}
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

    # Из этого говна можно понаделать функции в authorization_service для обработки ошибок
    # или запихнуть туда же под какой-нибудь новосозданный класс
    # ////////////////
    # Проверяем, существуют ли поля query_username в БД, если нет - кидаем ошибку
    # if not creds_login.username != query['username']:
    #
    #     print(creds_login.username)
    #
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid username or password"
    #     )
    #
    # # Проверяем, существует ли password (сравниваем в открытом виде, а надо хэшировать), если нет - кидаем ошибку
    # if not creds_login.password != query["password"]:
    #
    #     print(creds_login.password)
    #
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid username or password"
    #     )
    #
    #
    # # Проверяем, существует ли id юзера в БД, если нет - кидаем ошибку
    # if not creds_login.id != query['_id']:
    #
    #     print(creds_login.password)
    #
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid username or password"
    #
    # object_id = ObjectId(creds_login.id)
    # if creds_login.id != query["_id"]:
    #
    #     print(creds_login.id)
    #
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid _id"
    #     )
    # query = await async_collection.find_one({"_id": object_id})
    # if query:
    #     # Преобразуем ObjectId в строку
    #     query["_id"] = str(query["_id"])
    #     return query
    #
    #
    # # Генерируем токен доступа
    # # Токен хранит id юзера в uid
    # access_token = create_access_token(uid=str(query["_id"]))
    #
    #
    # # Cоздаю куки и записываю в них access_token
    # response.set_cookie(
    #     key=config.JWT_ACCESS_COOKIE_NAME,
    #     value=access_token,
    #     httponly=True,
    #     secure=True,
    #     samesite='lax',
    #     max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    #
    # # Если всё в порядке, редиректим на домашнюю страницу
    # # return {"message": "Login successful, cookie created!"}
    # return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)


# Функция для выхода из аккаунта и удаления куки
# Куки теперь не удаляются
@app.post("/logout")
async def logout(response: Response):
    # Удаляем куки с теми же параметрами, что и при установке
    response.delete_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        path="/",  # Убедитесь, что путь совпадает с тем, который использовался при установке
        domain='127.0.0.1',  # Укажите домен, если кука была установлена для конкретного домена
        secure=True,  # Убедитесь, что это совпадает с настройками куки
        httponly=True,  # Убедитесь, что это совпадает с настройками куки
        samesite="lax"  # Убедитесь, что это совпадает с настройками куки
    )

    # Возвращаем JSON-ответ об успешном выходе
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Logout successful"}
    )


# Функция для перехода по защищенному эндпоинту с проверкой Токена и ID
@app.get("/home", dependencies=[Depends(security.access_token_required)])
async def protected_route(request: Request):
    # Добавить обработку отсутствия куки

    return {"message": "You are authorized"}


'''response_model - явно указываем, в каком виде получим json-response; response_model_exclude_unset = True - юзер получит в json-response те поля, которые заполнял и все обязательные '''
'''response_model_exclude - указ те поля, которые хотим исключить из json-response'''
'''response_model_include - указ только те поля, которые хотим получить в json-response'''

# @app.post('/registration', response_model=UserId)
# def registration_user(item: RegistrationUser):
#     registration = item.dict()
#     registration['id'] = 112
#     # return UserId(**item.dict(), id=1)
#     return registration


# @app.get('/param')
# def param(q: list[str] = Query(['value_first', 'value_second'],
#                                min_length=2,
#                                max_length=255,
#                                description='Проверить документацию по Query и по передаче нескольких параметров в списке',
#                                deprecated=True)):
#     return q


# @app.get('/user/{id}')
# def search_user_id(id: int = Path(...,
#                                   gt=10,
#                                   le=100),
#                    pages: int = Query(None,
#                                       gt=0,
#                                       le=100,
#                                       title='Количество страниц',
#                                       description='Здесь описание')):
#     return {'id': id, 'pages': pages}


# @app.post('/stream_name')
# def stream_start(stream_name: StreamNaming, country: str = Body(...)):
#     '''Параметр Body нужен для того, чтобы не засорять URL новым параметром, но получать этот парамтр в ответе'''
#     return stream_name, {'country': country}


# @app.post('/stream')
# def stream_country(stream: StreamNaming = Body(..., embed=True)):
#     '''С помощью Body и флага embed=True укажем, что Pydantic-модель StreamingNaming должна быть вложена в json-объект stream'''
#     return stream


# Подготавливаем данные для сохранения
# update_data = {
#     "$set": {
#         "access_token": access_token,
#         "access_token_expires": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     }
# }
#
# Сохраняем токен в документе пользователя в БД
# await async_collection.update_one({'_id': query_username['_id']}, update_data)
