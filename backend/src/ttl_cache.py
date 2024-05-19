import time

CACHE = {}


def TTLCache(ttl):
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = (func, args, frozenset(kwargs.items()))
            if key in CACHE and time.time() - CACHE[key][0] < ttl:
                return CACHE[key][1]
            result = func(*args, **kwargs)
            CACHE[key] = [time.time(), result]
            return result

        return wrapper

    return decorator
