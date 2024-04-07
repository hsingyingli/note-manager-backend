from collections import namedtuple

Success = namedtuple(
    "Success",
    ["is_succeeded", "is_failed", "result"],
    defaults=[True, False, None],
)

Fail = namedtuple(
    "Fail",
    ["is_succeeded", "is_failed", "errors"],
    defaults=[False, True, None],
)


def async_monadic(func):
    async def wrap(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            if type(result) == Success or type(result) == Fail:
                return result
            return Success(result=result)
        except Exception as e:
            return Fail(errors=e)

    return wrap


def monadic(func):
    def wrap(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if type(result) == Success or type(result) == Fail:
                return result
            return Success(result=result)
        except Exception as e:
            return Fail(errors=e)

    return wrap
