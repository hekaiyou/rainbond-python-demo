import json
from flask import Flask, request
from base import parameter_verification
from rainbond_python.db_connect import DBConnect

app = Flask(__name__)
db = DBConnect(db='demo', collection='test')


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
    method = request.method

    if method == 'GET':
        cursor = db.get_collection().find()
        if not cursor.count():
            return '资源为空', 204, []
        data = list(cursor)
        return str(data), 200, []

    elif method == 'POST':
        verification = parameter_verification(request, ['name', 'age'])
        if verification['result']:
            parameter = verification['data']
            insert_dict = {'name': parameter['name'], 'age': parameter['age']}
            if db.write_one_docu(docu=insert_dict):
                return '新资源被创建', 201, []
            else:
                return '资源无法被创建', 500, []
        else:
            return verification['response']

    elif method == 'PUT':
        verification = parameter_verification(request, ['appid'])
        if verification['result']:
            return json.dumps(verification['data'], ensure_ascii=False)
        else:
            return verification['response']

    elif method == 'DELETE':
        verification = parameter_verification(request, ['appid'])
        if verification['result']:
            return json.dumps(verification['data'], ensure_ascii=False)
        else:
            return verification['response']


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
