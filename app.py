import json
from flask import Flask, request
from rainbond_python.db_connect import DBConnect
from rainbond_python.parameter import Parameter

app = Flask(__name__)
db = DBConnect(db='demo', collection='test')


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
    parameter = Parameter(request)

    if parameter.method == 'GET':
        cursor = db.mongo_collection.find()
        if not cursor.count():
            return '资源为空', 204, []
        data = list(cursor)
        return str(data), 200, []

    elif parameter.method == 'POST':
        if parameter.verification(checking=parameter.param_json, verify={'name': str, 'age': int}):
            param = parameter.param_json
            insert_dict = {'name': param['name'], 'age': param['age']}
            if db.write_one_docu(docu=insert_dict):
                return '新资源被创建', 201, []
            else:
                return '资源无法被创建', 500, []
        else:
            return '请求参数错误', 400, []

    elif parameter.method == 'PUT':
        return json.dumps(parameter.param_json, ensure_ascii=False), 200, []

    elif parameter.method == 'DELETE':
        return json.dumps(parameter.param_json, ensure_ascii=False), 200, []


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
