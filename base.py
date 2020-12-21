import os
import json
import pymongo

# RainBond: https://www.rainbond.com/docs/
# Restful API: https://www.runoob.com/w3cnote/restful-architecture.html
# 12 Factor: https://12factor.net/zh_cn/


def create_db_connection(db=None, collection=None, home=None, port=None):
    mongo_home = os.environ.get('MONGODB_HOST', home)
    mongo_port = os.environ.get('MONGODB_PORT', port)

    if not mongo_home or not mongo_port or not db or not collection:
        return {'result': False, 'data': ('MongoDB(组件)的组件连接信息是不完整的', 404, [])}

    try:
        mongo_client = pymongo.MongoClient(mongo_home, int(mongo_port))
        mongo_db = mongo_client[db]
        mongo_collection = mongo_db[collection]
        return {'result': True, 'data': mongo_collection}
    except Exception as err:
        return {'result': False, 'data': ('MongoDB(组件)出现未知错误: {0}'.format(err), 500, [])}


def parameter_verification(request, checking=None):
    if checking is None:
        checking = []
    method = request.method
    if method == 'GET':
        parameter = request.args
    else:
        parameter = json.loads(request.get_data(as_text=True))
    if not set(checking).issubset(set(parameter.keys())):
        return {'result': False, 'data': ('请求缺少必需的字段: {0}'.format(json.dumps(checking)), 400, [])}
    return {'result': True, 'data': parameter}
