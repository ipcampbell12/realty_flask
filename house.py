
import sqlite3
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required


class House(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field may not be left blank"
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field may not be left blank"
                        )
    parser.add_argument('square_feet',
                        type=int,
                        required=True,
                        help="This field may not be left blank"
                        )
    parser.add_argument('beds',
                        type=int,
                        required=True,
                        help="This field may not be left blank"
                        )
    parser.add_argument('baths',
                        type=int,
                        required=True,
                        help="This field may not be left blank"
                        )

    @jwt_required()
    def get(self, name):
        house = self.find_by_name(name)
        if house is not None:
            return house

        return {"message": "Item not found"}, 400

    @classmethod
    def find_by_name(cls, name):

        connection = sqlite3.connect('houses.db')
        cursor = connection.cursor()

        query = '''
            SELECT * FROM houses WHERE name = ?
        '''

        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row is not None:
            return {'house':
                    {'name': row[0],
                     'address': row[1],
                     'price': row[2],
                     'square_feet': row[3],
                     'beds': row[4],
                     'baths': row[5]
                     }
                    }

    @classmethod
    def insert(cls, house):

        connection = sqlite3.connect('houses.db')
        cursor = connection.cursor()

        insert_query = '''
            INSERT INTO houses 
            VALUES (?,?,?,?,?,?)
        '''

        cursor.execute(insert_query,
                       (
                           house['name'],
                           house['address'],
                           house['price'],
                           house['square_feet'],
                           house['beds'],
                           house['baths']
                       )
                       )

        connection.commit()
        connection.close()

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name) is not None:
            return {"message": f"A house with the name {name} already exists"}

        data = House.parser.parse_args()
        house = {
            "name": name,
            "address": data['address'],
            "price": data['price'],
            "square_feet": data['square_feet'],
            "beds": data['beds'],
            "baths": data['baths'],
        }

        try:
            self.insert(house)
        except:
            return {"Message": "An error occurred when inserting the house"}, 500

        return house, 201

    def put(self, house):
        data = House.parser.parse_args()

        if house is None:
            try:
                self.insert(house)
            except:
                {"Message": f"A house with the name {house} could not be found."}

        else:
            try:
                self.update(house)
            except:
                {"Message": f"A house with the name {house} could not be found."}

        return house

    def delete(self, name):

        connection = sqlite3.connect('houses.db')
        cursor = connection.cursor()

        delete_query = '''
                DELETE FROM houses
                WHERE name=?
            '''
        cursor.execute(delete_query, (name,))

        connection.commit()
        connection.close()
        return {"message": f"{name} has been deleted from the database"}

    def update(self, house):
        connection = sqlite3.connect('houses.db')
        cursor = connection.cursor()

        query = '''
        UPDATE houses
        SET address = ?,
        SET price = ?,
        SET square_feet = ?,
        SET beds = ?,
        SET baths = ?,
        WHERE name = ?
        '''

        cursor.execute(insert_query,
                       (
                           house['name'],
                           house['address'],
                           house['price'],
                           house['square_feet'],
                           house['beds'],
                           house['baths']
                       )
                       )

        connection.commit()
        connection.close()


class Houses(Resource):
    def get(self, houses):
        pass


""" 
{
    "address":"456 Potty lane",
    "price":45000,
    "squater_feet":120,
    "beds":12,
    "basths:15

}




"""
