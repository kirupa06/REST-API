from flask import *
from flask_restful import Resource, Api
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "API"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


class all_users(Resource):
    def get(self):  # retrieve users data
        try:
            con = mysql.connection.cursor()
            sql = "SELECT * FROM users"
            con.execute(sql)
            res = con.fetchall()
            return res

        except:
            return {"message": "Failed to select user"}, 400

        finally:
            con.close()

    def post(self):  # adding user
        try:
            data = request.json  # json format
            name = data['name']
            language = data['language']
            city = data['city']
            con = mysql.connection.cursor()
            sql = "INSERT INTO users(name,language,city) VALUES(%s,%s,%s)"
            con.execute(sql, [name, language, city])
            mysql.connection.commit()
            return {"message": 'User added successfully.'}, 200

        except:
            return {"message": "Failed to add user"}, 400

        finally:
            con.close()


api.add_resource(all_users, "/users")


class user(Resource):
    def get(self, id):  # fetching a user by his/her id
        try:
            con = mysql.connection.cursor()
            sql = "SELECT * FROM users WHERE id = %s"
            con.execute(sql, [id])  # [] is must
            res = con.fetchall()
            return res

        except:
            return {"message": "Failed to fetch the user"}, 400

        finally:
            con.close()

    def put(self, id):  # upating the user
        try:
            data = request.json
            name = data['name']
            language = data['language']
            city = data['city']
            con = mysql.connection.cursor()
            sql = "UPDATE users SET name = %s,language = %s, city = %s WHERE id = %s"
            con.execute(sql, [name, language, city, id])
            mysql.connection.commit()
            return {"message": "successfully updated the user"}, 200

        except:
            return {"message": "Failed to update user"}, 400

        finally:
            con.close()

    def delete(self, id):
        try:
            con = mysql.connection.cursor()
            sql = "DELETE FROM users where id = %s"
            con.execute(sql, [id])
            mysql.connection.commit()
            return {"message": "successfully deleted the user"}

        except:
            return {"message": "Failed to delete user"}, 400

        finally:
            con.close()


api.add_resource(user, '/users/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)
