
# 捕捉异常错误
def get_schema_errors(err):
    _e = err.messages
    msg = list(_e.values())[0][0]
    return msg