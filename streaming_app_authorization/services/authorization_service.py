from authx import AuthX, AuthXConfig
from starlette.responses import RedirectResponse
from fastapi import FastAPI
from streaming_app_authorization.database import db
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os
from fastapi import HTTPException, status, Request
from streaming_app_authorization.schemas import *
from streaming_app_authorization.database.db import *
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timedelta
from functools import wraps
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from authx.exceptions import MissingTokenError

app = FastAPI

load_dotenv()

# Конфиги для Авторизации через JWT
auth = AuthX()

config = AuthXConfig()
config.JWT_ALGORITHM = 'HS256'
config.JWT_SECRET_KEY = 'SK'
config.JWT_ACCESS_COOKIE_NAME = 'access_cookie'
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# Функция создания токена доступа
# Токен хранит id юзера в uid
def create_access_token(uid: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": uid, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


def verify_user(func):
    @wraps(func)
    async def wrapper(user_id: str, user_token: str, *args, **kwargs):
        # Проверяем, существуют ли поля user_id и token в запросе, если нет - кидаем ошибку
        if not user_id or not user_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id and token are required"
            )

        # Преобразуем строку user_id в ObjectId
        try:
            object_id = ObjectId(user_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user_id"
            )

        # Ищем пользователя в базе данных
        user_verification = await async_collection.find_one({"_id": object_id})

        # Проверяем, существует ли ID пользователя, если нет - кидаем ошибку
        if not user_verification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Преобразуем object_id обратно в строку
        user_verification["_id"] = str(user_verification["_id"])

        # Проверяем, совпадает ли токен, если нет - кидаем ошибку
        if user_verification.get("token") != user_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        # Проверяем, не истек ли токен, если нет - кидаем ошибку
        if user_verification.get("token_expires") < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )

        # Если токен валиден, вызываем оригинальную функцию
        # return await func(request, *args, **kwargs)
        return await func(user_id=user_id, user_token=user_token, *args, **kwargs)

    return wrapper


# Асинхронная функция проверки наличия id пользователя в БД (необязательная)
# Должен лезть в БД, искать юзернейм (или другое поле), а потом искать id
# @app.get("/add_to_database/{item_id}")
async def find_user_id(item_id: str):
    try:
        # Преобразуем строку в ObjectId
        object_id = ObjectId(item_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid item ID")

    # Ищем элемент в коллекции
    query = await async_collection.find_one({"_id": object_id})
    if query:
        # Преобразуем ObjectId в строку
        query["_id"] = str(query["_id"])
        return query
    raise HTTPException(status_code=404, detail="Item not found in MongoDB")



# Это обработчик исключения от AuthX.
# AuthX выводит ошибку в терминал, а не в OpenAPI
# Проблема. Если юзер самостоятельноо удаляет куки, то при успешной авторизации и редиректе на /home они не подкидываются заново
#
# @app.exception_handler(MissingTokenError)
# async def missing_token_exception_handler(request: Request, exc: MissingTokenError):
#     return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


# security = HTTPBearer()
#
# Функция извлечения токена из куки
# При использовании security = HTTPBearer()
# async def get_current_user(request: Request):
#     # Извлекаем токен из куки
#     access_token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
#     if not access_token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated"
#         )
#
#     try:
#         # Декодируем токен
#         payload = jwt.decode(access_token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token"
#             )
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token expired"
#         )
#     except jwt.InvalidTokenError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token"
#         )
#
#     # Возвращаем идентификатор пользователя
#     return user_id
