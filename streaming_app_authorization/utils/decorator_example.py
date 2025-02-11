# def decorator(a_func):
#     def wrap_function():
#         print("Какая-то логика перед исполнением a_func()")
#         a_func()
#         print("Какая-то логика после исполнения	a_func()")
#
#     return wrap_function
#
#
# @decorator
# def default_function():
#     return print('I need decorator wrapper!')
#
#
# default_function()

# Вызываем без @decorator
# decorator_wrapper_default_function = decorator(default_function)
# decorator_wrapper_default_function()

from functools import wraps


# def my_decorator(func):
#     # @wraps(func) копирует все метаданные обёртываемой функции в обёрточную функцию wrapper.
#     # Так они сохранятся при декорировании.
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print("До вызова функции")
#         result = func(*args, **kwargs)
#         print("После вызова функции")
#         return result
#     return wrapper
#
#
# @my_decorator
# def my_function():
#     """Это документация оригинальной функции."""
#     print("Функция выполнена")
#
#
# print(my_function.__name__)
# print(my_function.__doc__)
