from japronto.response import JsonResponse


def resp_handler(func):
    def wrapper(*args, **kwargs):
        err_body = {
            'err_code': 0,
            'err_msg': 'ok'
        }
        try:
            resp = func(*args, **kwargs)
            resp.json.update(**err_body)
        except Exception as e:
            err_body.update(
                err_code=getattr(e, 'code', 400),
                err_msg=str(e.args[0])
            )
            resp = JsonResponse(json=err_body)
        req = args[2]
        return req.Response(**dict(resp))

    return wrapper
