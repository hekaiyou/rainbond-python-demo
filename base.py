import json

# RainBond: https://www.rainbond.com/docs/
# Restful API: https://www.runoob.com/w3cnote/restful-architecture.html
# 12 Factor: https://12factor.net/zh_cn/


def parameter_verification(request, checking=None):
    if checking is None:
        checking = []
    method = request.method
    if method == 'GET':
        parameter = request.args
    else:
        parameter = json.loads(request.get_data(as_text=True))
    if not set(checking).issubset(set(parameter.keys())):
        return {'result': False, 'response': ('请求缺少必需的字段: {0}'.format(json.dumps(checking)), 400, [])}
    return {'result': True, 'data': parameter}
