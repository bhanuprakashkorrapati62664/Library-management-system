from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.library

@app.route('/')
def home():
    books_count = db.books.count_documents({})
    available_count = db.books.count_documents({"available": True})
    borrowed_count = books_count - available_count
    return render_template('home.html', books_count=books_count, available_count=available_count, borrowed_count=borrowed_count)

@app.route('/books')
def books():
    books = list(db.books.find({}))
    return render_template('books.html', books=books)

@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    if request.method == 'POST':
        book_data = {
            "title": request.form['title'],
            "author": request.form['author'],
            "isbn": request.form['isbn'],
            "published_year": request.form['published_year'],
            "available": True  # Default to available when added
        }
        db.books.insert_one(book_data)
        return redirect(url_for('books'))
    return render_template('add_book.html')

if __name__ == '__main__':
    app.run(debug=True)
