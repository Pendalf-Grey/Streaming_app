# from fastapi import FastAPI, Request, status
# from fastapi.responses import RedirectResponse
# from fastapi.exceptions import HTTPException
#
#
# app = FastAPI
#
#
# @app.exception_handler(status.HTTP_401_UNAUTHORIZED)
# async def unauthorized_exception_handler(request: Request, exc: HTTPException):
#     # Перенаправляем на страницу авторизации
#     return RedirectResponse(url="/login")
