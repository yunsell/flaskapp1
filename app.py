from flask import Flask, request, jsonify
from flask_restx import Resource, Api
import mariadb

app = Flask(__name__)
api = Api(app)
app.debug = True

todos = "SELECT email,user_name from drcms.`user` where id = {};"
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
        dictResult: dict = dict()

        sql = "select id,email,user_name from user;"

        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(sql)
            user = cur.fetchall()

            dictResult = [dict(zip([key[0] for key in cur.description], row)) for row in user]

        except Exception as e:
            print(e)

        return jsonify(dictResult)

    def post(self):
        global count
        global todos

        sql = f"INSERT INTO drcms.user (email, password, user_name, grade, created_at, updated_at)" \
              f"VALUES ('test{count}@test.com', '1234', 'tester{count}', '9', now(), now())"

        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()

        except Exception as e:
            print(e)

        idx = count
        count += 10
        todos[idx] = request.json.get('data')

        return {
            'id': idx,
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