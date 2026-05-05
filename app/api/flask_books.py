from flask import request
from flask_restful import Resource
from app.repository.mongo_repo import MongoBookRepository
from app.database import db

class BookListResource(Resource):
    def get(self):
        """
        Get list of books
        ---
        parameters:
          - name: limit
            in: query
            type: integer
            default: 10
          - name: offset
            in: query
            type: integer
            default: 0
          - name: author
            in: query
            type: string
          - name: status
            in: query
            type: string
        responses:
          200:
            description: A list of books
        """
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        author = request.args.get('author')
        status = request.args.get('status')
        
        repo = MongoBookRepository(db)
        books = repo.get_all(db, limit, offset, status, author)
        total = db.books.count_documents({})
        
        return {
            "items": books,
            "total": total,
            "limit": limit,
            "offset": offset
        }, 200

    def post(self):
        """
        Create a new book
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Book
              required:
                - title
                - author
                - year
              properties:
                title:
                  type: string
                author:
                  type: string
                year:
                  type: integer
                description:
                  type: string
                status:
                  type: string
        responses:
          201:
            description: Book created
        """
        data = request.get_json()
        repo = MongoBookRepository(db)
        new_book = repo.add(db, data)
        return new_book, 201

class BookResource(Resource):
    def get(self, book_id):
        """
        Get a book by ID
        ---
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Book details
          404:
            description: Book not found
        """
        repo = MongoBookRepository(db)
        book = repo.get_by_id(db, book_id)
        if not book:
            return {"message": "Book not found"}, 404
        return book, 200

    def delete(self, book_id):
        """
        Delete a book
        ---
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          204:
            description: Book deleted
          404:
            description: Book not found
        """
        repo = MongoBookRepository(db)
        success = repo.delete(db, book_id)
        if not success:
            return {"message": "Book not found"}, 404
        return "", 204