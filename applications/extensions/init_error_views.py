from flask import  jsonify
from werkzeug.exceptions import HTTPException
from applications.common.utils.http import APIException, APIResponse,ServerError

def init_error_views(app):
    # @app.errorhandler(403)
    # def page_not_found(e):
    #     return jsonify({"code": -1, "msg": 403, "data": None}), 403

    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return jsonify({"code": -1, "msg": 404, "data": None}), 403

    # @app.errorhandler(500)
    # def internal_server_error(e):
    #     return jsonify({"code": -1, "msg": 403, "data": None}), 403

    # # Return validation errors as JSON
    # @app.errorhandler(422)
    # @app.errorhandler(400)
    # def handle_error(err):
    #     headers = err.data.get("headers", None)
    #     messages = err.data.get("messages", ["Invalid request."]).get('json')
    #     print(err.data.get("messages"))
    #     print(messages.items())
    #     msg = ''

    #     for i in messages.items():
    #         msg = str(i[0]) + str(i[1][0])
    #         break

    #     if headers:
    #         return jsonify({"code": -1, "msg": msg, "data": None})
    #     else:
    #         return jsonify({"code": -1, "msg": msg, "data": None})

    @app.errorhandler(Exception)
    def framework_error(e):
        print("异常信息：",e)
        # 判断异常是不是APIException
        if isinstance(e, APIException):
            return e
        # 判断异常是不是HTTPException
        if isinstance(e, HTTPException):
            code = e.code
            # 获取具体的响应错误信息
            msg = e.description
            return APIException(code = code, msg = msg)
        # 异常肯定是Exception
        else:
            # 如果是调试模式,则返回e的具体异常信息。否则返回json格式的 APIException 对象！
            # 针对于异常信息，我们最好用日志的方式记录下来。
            if app.config["DEBUG"]:
                return ServerError()
            raise
