import logging
import functools

def errors_catching_async(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.error("Exception", exc_info=e) 
            return e
    return wrapper

def errors_catching(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error("Exception", exc_info=e) 
            return e
    return wrapper