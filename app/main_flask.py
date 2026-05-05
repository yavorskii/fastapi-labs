from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from app.api.flask_books import BookResource, BookListResource

app = Flask(__name__)
api = Api(app)

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Library API - Lab 5",
        "description": "API на Flask-RESTful з використанням Swagger (Flasgger)",
        "version": "5.0.0"
    },
    "host": "localhost:8000",
    "basePath": "/",
    "schemes": [
        "http"
    ]
})

api.add_resource(BookListResource, '/books')
api.add_resource(BookResource, '/books/<string:book_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)