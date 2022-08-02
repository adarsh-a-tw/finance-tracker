from functools import wraps

from fastapi import Request


def login_required(view_func):
    @wraps(view_func)
    def func(request: Request, *args, **kwargs):
        if request.headers.get('x-api-token'):  # todo: implement jwt token and db check
            return view_func(request, *args, **kwargs)

        return {"Error": 404}

    return func
