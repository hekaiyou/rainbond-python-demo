import json
from flask import Flask, request
from base import create_db_connection, parameter_verification

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
    # 安全地连接MongoDB(组件)
    connection = create_db_connection(db='demo', collection='test')
    # 开发时连接本地数据库，但是提交代码时请注释掉
    # connection = create_db_connection(db='demo', collection='test', home='localhost', port='27017')
    if not connection['result']:
        return connection['data']
    # MongoDB(组件)中 demo 数据库的 test 集合对象
    collection = connection['data']

    method = request.method

    if method == 'GET':
        cursor = collection.find()
        if not cursor.count():
            return '资源为空', 204, []
        data = list(cursor)
        return str(data), 200, []

    elif method == 'POST':
        verification = parameter_verification(request, ['name', 'age'])
        if verification['result']:
            parameter = verification['data']
            insert_dict = {'name': parameter['name'], 'age': parameter['age']}
            collection.insert_one(insert_dict)
            return '新资源被创建', 201, []
        else:
            return verification['data']

    elif method == 'PUT':
        verification = parameter_verification(request, ['appid'])
        if verification['result']:
            return json.dumps(verification['data'], ensure_ascii=False)
        else:
            return verification['data']

    elif method == 'DELETE':
        verification = parameter_verification(request, ['appid'])
        if verification['result']:
            return json.dumps(verification['data'], ensure_ascii=False)
        else:
            return verification['data']


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
