import json
from flask import Flask, request
from base import create_db_connection, parameter_verification

app = Flask(__name__)
db_client = create_db_connection()


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
    method = request.method

    db = db_client['demo']
    collection = db['test']

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
