import sqlite3
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource,Api,reqparse

data_base = 'library.db'

app = Flask(__name__)
CORS(app)
api = Api(app)

class BookDataBase(Resource):
    def __init__(self):
        self.con = sqlite3.connect(data_base)
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Books (book_id integer PRIMARY KEY AUTOINCREMENT,book_name text NOT NULL,author_id integer NOT NULL,FOREIGN KEY (author_id) REFERENCES author(author_id));''')
        #cur.execute('''CREATE TABLE IF NOT EXISTS Author (author_id integer PRIMARY KEY AUTOINCREMENT,author_name text NOT NULL,author_age integer NOT NULL);''')         
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('book_name')
        parser.add_argument('author_id')
        data = parser.parse_args()

        param_attribute = ''
        param = ''

        if data['book_name']:
            param_attribute = 'book_name'
            param = data['book_name']

        elif data['author_id']:
            param_attribute = 'author_id'
            param = data['author_id']

        else:
            return {
                'status': 'error',
                'reason': 'invalid query'
            }

        self.cur.execute('''SELECT * FROM Books where {}='{}';'''.format(param_attribute, param))
        return {
            "status": "success",
            "data": self.cur.fetchall()
        }


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('book_name')
        parser.add_argument('author_id')   
        data = parser.parse_args()
        
        self.cur.execute('''INSERT INTO Books(book_name,author_id) VALUES ('{}',{})'''.format(data['book_name'],data['author_id']))
        self.con.commit()

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('book_id')
        parser.add_argument('book_name')
        parser.add_argument('author_id')   
        data = parser.parse_args()

        if not data['book_id']:
            return {
                'status': 'error',
                'reason': 'book id required'
            }

        if data['book_name'] and data['author_id']:
            self.cur.execute('''UPDATE Books SET book_name='{}', author_id={} WHERE book_id={}'''.format(data['book_name'],data['author_id'],data['book_id']))

        elif data['book_name']:
            self.cur.execute('''UPDATE Books SET book_name='{}' WHERE book_id={}'''.format(data['book_name'],data['book_id']))

        elif data['book_id']:
            self.cur.execute('''UPDATE Books SET author_id ={} WHERE book_id={}'''.format(data['author_id'],data['book_id']))

        else:
            return {
                'status': 'error',
                'reason': 'invalid query'
            }
        
        self.con.commit()

        return {
            'status': 'success'
        }


api.add_resource(BookDataBase,'/api/book')

class AuthorDataBase(Resource):
    def __init__(self):
        self.con = sqlite3.connect(data_base)
        self.cur = self.con.cursor()
        #cur.execute('''CREATE TABLE IF NOT EXISTS Books (book_id integer PRIMARY KEY AUTOINCREMENT,book_name text NOT NULL,author_id integer NOT NULL,FOREIGN KEY (author_id) REFERENCES author(author_id));''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Author (author_id integer PRIMARY KEY AUTOINCREMENT,author_name text NOT NULL,author_age integer NOT NULL);''')         
    
    def get(self):
        #print("Get")
        parser = reqparse.RequestParser()
        parser.add_argument('author_name')
        parser.add_argument('author_age')   
        data = parser.parse_args()

        param_attribute = ''
        param = ''

        if data['author_name']:
            param_attribute = 'author_name'
            param = data['author_name']

        elif data['author_age']:
            param_attribute = 'author_age'
            param = data['author_age']

        else:
            return {
                'status': 'error',
                'reason': 'invalid query'
            }

        self.cur.execute('''SELECT * FROM Author where {}='{}';'''.format(param_attribute, param))

        return {
            "status": "success",
            "data": self.cur.fetchall()
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('author_name')
        parser.add_argument('author_age')   
        data = parser.parse_args()
        
        self.cur.execute('''INSERT INTO Author(author_name,author_age) VALUES ('{}',{})'''.format(data['author_name'],data['author_age']))
        self.con.commit()

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('author_id')
        parser.add_argument('author_name')
        parser.add_argument('author_age')   
        data = parser.parse_args()

        if not data['author_id']:
            return {
                'status': 'error',
                'reason': 'author id required'
            }

        if data['author_name'] and data['author_age']:
            self.cur.execute('''UPDATE Author SET author_name='{}', author_age={} WHERE author_id={}'''.format(data['author_name'],data['author_age'],data['author_id']))

        elif data['author_name']:
            self.cur.execute('''UPDATE Author SET author_name='{}' WHERE author_id={}'''.format(data['author_name'],data['author_id']))

        elif data['author_age']:
            self.cur.execute('''UPDATE Author SET author_age={} WHERE author_id={}'''.format(data['author_age'],data['author_id']))

        else:
            return {
                'status': 'error',
                'reason': 'invalid query'
            }
        
        self.con.commit()

        return {
            'status': 'success'
        }

api.add_resource(AuthorDataBase,'/api/author')


if __name__ == '__main__':
    app.run(debug = True)

