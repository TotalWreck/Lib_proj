from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


app = Flask(__name__)


# Configuring the SQLite database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"


# SQLAlchemy database object
db = SQLAlchemy(app)


# Object Classes
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, year_published, stock):
        self.title = title
        self.author = author
        self.year_published = year_published
        self.stock = stock

    loans = relationship('Loan', backref='book', lazy=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    loans = relationship('Loan', backref='user', lazy=True)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    loan_date = db.Column(db.Integer, nullable=False)
    loan_length = db.Column(db.Integer, nullable=False)
    returned = db.Column(db.Boolean, default=False)

    def __init__(self, book_id, user_id, loan_date, loan_length):
        self.book_id = book_id
        self.user_id = user_id
        self.loan_date = loan_date
        self.loan_length = loan_length
        self.returned = False


# Create the database tables
with app.app_context():
    db.create_all()


# index.html route
@app.route('/')
def index():
    return render_template("index.html")

# Route to list all books
@app.route('/books', methods=["GET"])
def list_books():
    books = Book.query.all()
    book_list = []

    for book in books:
        book_data = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year_published": book.year_published,
            "stock": book.stock
        }
        book_list.append(book_data)

    response_data = {"books": book_list}

    if "application/json" in request.headers.get("Accept"):
        return jsonify(response_data)
    else:
        return render_template('book_list.html', books=response_data)

# Route to retrieve or delete a specific book
@app.route('/books/<int:book_id>', methods=["GET", "PUT"])
def retrieve_or_delete_book(book_id):
    book = Book.query.get(book_id)
    
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if request.method == "PUT":
        book.title = "DELETED BOOK"
        book.author = "n/a"
        book.year_published = "n/a"
        book.stock = 0
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"})

    book_data = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year_published": book.year_published,
        "stock": book.stock
    }

    response_data = {"book": book_data}

    if "application/json" in request.headers.get("Accept"):
        return jsonify(response_data)
    else:
        return render_template('book_id.html', book=response_data)

# Route to add a new book
@app.route('/books/add', methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        year_published = request.form.get("year_published")
        stock = request.form.get("stock")

        if title and author and year_published and stock:
            new_book = Book(title=title, author=author, year_published=int(year_published), stock=int(stock))
            db.session.add(new_book)
            db.session.commit()
            response = {"message": "Book added successfully", "status": "success"}
            return jsonify(response), 200

        response = {"message": "Invalid or missing data. Please fill in all fields with valid data.", "status": "failure"}
        return jsonify(response), 400

    return render_template("book_add.html")


# Route to edit a book by ID
@app.route('/books/<int:book_id>/edit', methods=["PUT"])
def edit_book(book_id):
    data = request.json
    title = data.get("title")
    author = data.get("author")
    year_published = data.get("year_published")
    stock = data.get("stock")
    book = Book.query.get(book_id)

    if not book:
        return jsonify({"error": "Book not found"}), 404
    if title:
        book.title = title
    if author:
        book.author = author
    if year_published:
        book.year_published = year_published
    if stock:
        book.stock = stock
    db.session.commit()
    return jsonify({"message": "Book edited successfully"})


# Route to get all users
@app.route('/users', methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = []

    for user in users:
        user_data = {
            "id": user.id,
            "name": user.name,
            "city": user.city,
            "age": user.age
        }
        user_list.append(user_data)

    response_data = {"users": user_list}

    if "application/json" in request.headers.get("Accept"):
        return jsonify(response_data)
    else:
        return render_template('user_list.html')


# Route to retrieve or delete a specific book
@app.route('/users/<int:user_id>', methods=["GET", "PUT"])
def retrieve_or_delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == "PUT":
        # Delete the user (you can customize this as needed)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})

    user_data = {
        "id": user.id,
        "name": user.name,
        "city": user.city,
        "age": user.age
    }

    response_data = {"user": user_data}

    if "application/json" in request.headers.get("Accept"):
        return jsonify(response_data)
    else:
        return render_template('user_id.html', user=response_data)


# Route to add a new user
@app.route('/users/add', methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form.get("name")
        city = request.form.get("city")
        age = request.form.get("age")

        if name and city and age:
            new_user = User(name=name, city=city, age=int(age))
            db.session.add(new_user)
            db.session.commit()
            response = {"message": "User added successfully", "status": "success"}
            return jsonify(response), 200

        response = {"message": "Invalid or missing data. Please fill in all fields with valid data.", "status": "failure"}
        return jsonify(response), 400

    return render_template("user_add.html")


# Route to edit a user by ID
@app.route('/users/<int:user_id>/edit', methods=["PUT"])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    city = data.get("city")
    age = data.get("age")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if name:
        user.name = name
    if city:
        user.city = city
    if age:
        user.age = age
    db.session.commit()
    return jsonify({"message": "User updated successfully"})


# Route to get all loans
@app.route('/loans', methods=["GET"])
def get_loans():
    loans = Loan.query.all()
    loan_list = []
    for loan in loans:
        loan_data = {
            "id": loan.id,
            "book_id": loan.book_id,
            "user_id": loan.user_id,
            "loan_date": loan.loan_date,
            "loan_length": loan.loan_length
        }
        loan_list.append(loan_data)
    return jsonify({"loans": loan_list})


# Route to add a new loan
@app.route('/loans/add', methods=["POST"])
def add_loan():
    data = request.json
    book_id = data.get("book_id")
    user_id = data.get("user_id")
    loan_date = data.get("loan_date")
    loan_length = data.get("loan_length")
    returned = False
   
    if book_id and user_id and loan_date and loan_length:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({"error": "Book not found"}), 404
       
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
       
        if book.stock <= 0:
            return jsonify({"error": "No more copies of this book in stock"}), 400
       
        if 1 <= loan_length <= 365:
            new_loan = Loan(book_id=book_id, user_id=user_id, loan_date=loan_date, loan_length=loan_length)
            db.session.add(new_loan)
            db.session.commit()
           
            book.stock -= 1
            db.session.commit()
           
            return jsonify({"message": "Loan added successfully"})
        else:
            return jsonify({"error": "Length of loan is invalid, must be between 1 and 365 days."})
    else:
        return jsonify({"error": "Book ID, user ID, loan date, and loan length are required."}), 400


# Route to edit a loan by ID
@app.route('/loans/<int:loan_id>/edit', methods=["PUT"])
def edit_loan(loan_id):
    data = request.json
    book_id = data.get("book_id")
    user_id = data.get("user_id")
    loan_date = data.get("loan_date")
    loan_length = data.get("loan_length")
    returned = data.get("returned")

    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404

    previous_returned = loan.returned
   
    if book_id:
        loan.book_id = book_id
    if user_id:
        loan.user_id = user_id
    if loan_date:
        loan.loan_date = loan_date
    if loan_length:
        loan.loan_length = loan_length
    if returned is not None:
        loan.returned = returned

    db.session.commit()

    if not previous_returned and loan.returned:
        book = Book.query.get(loan.book_id)
        if book:
            book.stock += 1
            db.session.commit()

    return jsonify({"message": "Loan edited successfully"})


# Route to delete a loan by ID
@app.route('/loans/<int:loan_id>/delete', methods=["PUT"])
def delete_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404
    loan.book_id = "DELETED LOAN"
    loan.user_id = "null"
    loan.loan_date = "null"
    loan.loan_length = "null"
    loan.returned = "null"
    db.session.commit()
    return jsonify({"message": "Loan deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
