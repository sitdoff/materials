import functools
import time

from django.db import connection, reset_queries


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Функция: {func.__name__}")
        print(f"Число запросов в БД: {end_queries - start_queries}")
        print(f"Время выполнения функции: {(end - start):.2f} сек")
        return result

    return inner_func
