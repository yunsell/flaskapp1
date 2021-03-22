from flask import Flask, request, jsonify
from flask_restx import Resource, Api
import mariadb

app = Flask(__name__)
api = Api(app)
app.debug = True

todos = {}
count = 1

def get_conn():
    conn = mariadb.connect(
        user="drsong",
        password="drs12#",
        host="192.168.0.99",
        port=3306,
        database="drcms"
    )
    return conn

@api.route('/todos')
class TodoPost(Resource):
    def get(self):
        return jsonify(todos)

    def post(self):
        global count
        global todos

        idx = count
        count += 1
        todos[idx] = request.json.get('data')

        return {
            'todo_id': idx,
            'data': todos[idx]
        }


@api.route('/todos/<int:todo_id>')
class TodoSimple(Resource):
    def get(self, todo_id):
        return {
            'todo_id': todo_id,
            'data': todos[todo_id]
        }

    def put(self, todo_id):
        todos[todo_id] = request.json.get('data')
        return {
            'todo_id': todo_id,
            'data': todos[todo_id]
        }

    def delete(self, todo_id):
        del todos[todo_id]
        return {
            "delete": "success"
        }


if __name__ == "__main__":
    app.run()