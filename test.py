from flask import Flask, request, jsonify
import mariadb

app = Flask(__name__)
app.debug = True

def get_conn():
    conn = mariadb.connect(
        user="drsong",
        password="drs12#",
        host="192.168.0.99",
        port=3306,
        database="drcms"
    )
    return conn

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/user", methods=['GET'])
def user():
    dictResult : dict = dict()

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


@app.route("/user/<int:user_id>", methods=['GET'])
def user_read(user_id):
    dictResult: dict = dict()
    userid = user_id
    sql = f"select * from user where id={userid}"

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        user = cur.fetchall()

        dictResult = [dict(zip([key[0] for key in cur.description], row)) for row in user]

    except Exception as e:
        print(e)

    return jsonify(dictResult)


@app.route("/user/<int:user_id>", methods=['POST'])
def user_create(user_id):
    userid = user_id
    sql = f"INSERT INTO drcms.user (email, password, user_name, grade, created_at, updated_at)" \
          f"VALUES ('test{userid}@test.com', '1234', 'tester{userid}', '9', now(), now())"

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)

    return f"tester{userid} 아이디로 생성 성공 !!!"


@app.route("/user/<int:user_id>", methods=['DELETE'])
def user_delete(user_id):
    userid = user_id
    sql = f"delete from user where id={userid}"

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)

    return f"Id {userid} 번 아이디 삭제 성공 !!!"


@app.route("/user/update/<int:user_id>", methods=['PUT'])
def user_update(user_id):
    userid = user_id
    sql = f"update drcms.user set user_name = 'testupdate' where id={userid}"

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)

    return f"Id {userid} 번 아이디 변경 성공 !!!"
if __name__ == '__main__':
    app.run()
