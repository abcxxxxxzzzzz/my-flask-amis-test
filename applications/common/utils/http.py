import json

from flask import request
from werkzeug.exceptions import HTTPException
import enum
from flask import jsonify


class APIException(HTTPException):
    """
    为了使代码简洁, 首先定义一个最基本的类, 供其它类继承, 这个自定义的APIException继承HTTPException.
    1. 为了返回特定的body信息, 需要重写get_body;
    2. 为了指定返回类型, 需要重写get_headers.
    3. 为了接收自定义的参数, 重写了__init__;
    4. 同时定义了类变量作为几个默认参数.(code500和error_code:999 均表示未知错误, error_code表示自定义异常code)
    """
    code = 500
    msg = 'sorry，internal error'
    data = ''

    # 自定义需要返回的信息，在初始化完成并交给父类

    def __init__(self, msg=None, code=None,  data=None, headers=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if data:
            self.data = data
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        body = dict(
            code=self.code,
            msg=self.msg,
            request=request.method + ' ' + self.get_url_no_parm(),
            data=self.data
        )
        # sort_keys 取消排序规则，ensure_ascii 中文显示
        text = json.dumps(body, sort_keys=False, ensure_ascii=False)
        return text

    def get_headers(self, environ=None, scope=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_parm():
        full_path = str(request.path)
        return full_path


# -------------------------------------- raise 自定义错误返回
class Success(APIException):
    # code = 201
    code = 200
    msg = '成功'
    error_code = 0
    data = None
 
 
class DeleteSuccess(APIException):
    # code = 200
    code = 201
    msg = '删除成功'
    error_code = 1
    data = None
 
 
class UpdateSuccess(APIException):
    # code = 200
    code = 202
    msg = '更新成功'
    error_code = 2
    data = None
 
 
class ServerError(APIException):
    code = 500
    msg = '服务器内部错误'
    error_code = 999
 
 
class ParameterException(APIException):
    code = 400
    msg = '无效参数'
    error_code = 1000

 
class NotFound(APIException):
    code = 404
    msg = '未找到'
    error_code = 1001
 
 
class AuthFailed(APIException):
    code = 401
    msg = '认证失败'
    error_code = 1005
 
 
class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = '权限不足'

    

class Code(enum.Enum):
    # 请求状态吗
    SUCCESS = 0
    FAILED = -1


# --------------------------------------------------------------------------


class APIResponse(APIException):

    def SUCCESS(data=None, msg='ok',*args, **kwargs):
        return jsonify(code=Code.SUCCESS.value, msg=msg, data=data, *args, **kwargs)

    def FAILED(msg="", data=None):
        return jsonify(code=Code.FAILED.value, msg=msg, data=data)