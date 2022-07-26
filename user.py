import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.passowrd = password

    @classmethod
    def find_by_username(cls, username):

        connection = sqlite3.connect('house.db')
        cursor = connection.cursor()

        search_query = ''''
            SELECT * FROM houses WHERE username = ?
        '''

        result = cursor.execute(search_query, (username,))
        row = result.fetchone()

        if row is not None:
            user = cls(row[0], row[1], row[2])
        else:
            return None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):

        connection = sqlite3.connect('house.db')
        cursor = connection.cursor()

        search_query = ''''
            SELECT * FROM houses WHERE id = ?
        '''

        result = cursor.execute(search_query, (_id,))
        row = result.fetchone()

        if row is not None:
            user = cls(row[0], row[1], row[2])
        else:
            return None

        connection.close()
        return user

    class UserRegister(Resource):
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                            type=str,
                            required=True,
                            help="This field cannot be left blank"
                            )
        parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field cannot be left blank"
                            )

        def post(self):
            data = UserRegister.parser.parse_args()

            if User.find_by_username(data['username']) is not None:
                return {"message": "This username already exists"}, 400

            connection = sqlite3.connect('houses.db')
            cursor = connection.cursor()

            insert_query = '''
                INSERT INTO houses
                VALUES (NULL,?,?)
            '''

            cursor.execute(insert_query, (data['username'], data['password']))

            connection.commit()
            connection.close()

            return {"message": "User bas been created sucessfully"}, 201
