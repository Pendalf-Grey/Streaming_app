from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional



class LoginUserSchema(BaseModel):
    '''Схема для валидации полей во время авторизации'''
    username: str
    password: str
    id: str


class RegistrationUserSchema(BaseModel):
    '''Схема для валидации полей во время регистрации'''
    username: str
    password: str
    # email: EmailStr
    # hashed_password: str
    # disabled: Optional[bool] = False
    # age: int = Field(..., gt=10, le=100, description='Дополнительная логика валидации. Простая')
    # sex: str = None

    # @field_validator('age')
    # def user_check_age(cls, value):
    #     '''Дополнительная валидация полей'''
    #     if value <= 17:
    #         raise ValueError('Пользователь должен быть совершеннолетним!')
    #     return value


# class UserInBdSchema(RegistrationUserSchema):
#     id: str
