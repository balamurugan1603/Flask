from flask import Flask, request
from flask_restful import Api, Resource
from models import db, BookModel

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


class BookList(Resource):
    def get(self):
        books = BookModel.query.all()
        return {"books": [book.json() for book in books]}

    def post(self):
        data = request.get_json()
        book = BookModel(data["name"], data["price"], data["author"])
        db.session.add(book)
        db.session.commit()
        return book.json(), 201


class Book(Resource):
    def get(self, name):
        book = BookModel.query.filter_by(name=name).first()
        if book:
            return book.json()
        return {"message": "book not found"}, 404

    def put(self, name):
        book = BookModel.query.filter_by(name=name).first()
        data = request.get_json()

        if book:
            book.price = data["price"]
            book.author = data["author"]
        else:
            book = BookModel(name=name, **data)

        db.session.add(book)
        db.session.commit()
        return book.json()

    def delete(self, name):
        book = BookModel.query.filter_by(name=name).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return {"message": "delete successful"}, 201
        else:
            return {"message": "book not found"}, 404


api.add_resource(BookList, "/books")
api.add_resource(Book, "/book/<string:name>")


if __name__ == "__main__":
    app.run("localhost", port=5000)
