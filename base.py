import os
import json
import pymongo

# RainBond: https://www.rainbond.com/docs/
# Restful API: https://www.runoob.com/w3cnote/restful-architecture.html
# 12 Factor: https://12factor.net/zh_cn/


def create_db_connection(home_kye='MONGODB_HOST', port_kye='MONGODB_PORT'):
    mongo_home = os.environ.get(home_kye, None)
    mongo_port = os.environ.get(port_kye, 27017)

    if not mongo_home or not mongo_port:
        print('MongoDB(组件)的组件连接信息是不完整的')
    try:
        mongo_client = pymongo.MongoClient(mongo_home, int(mongo_port))
        return mongo_client
    except Exception as err:
        print('MongoDB(组件)出现未知错误: {0}'.format(err))


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
