import os
from crypt import methods

from datetime import datetime

from flask import Flask, jsonify, request, flash, url_for, redirect, render_template

from data_models import db, Author, Book


#'initialise flask'
app = Flask(__name__)



# Set the secret key for sessions (important for flash messages)
app.secret_key = 'flask_orm'
#setting the database URI

# Absolute path for the database file in the 'data' directory
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'library.sqlite')

# Configure the database URI using the absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'isolation_level': None
}


#connect flask app to flask-sqlalchemy code.
db.init_app(app)



@app.route("/add_author", methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
       # Get the author data from the form
       name = request.form.get('name').strip()
       birth_date_str= request.form.get('birthdate')
       death_date_str = request.form.get('date_of_death')
       # Check if the name is provided
       if not name:
           flash('Author name is required.', 'danger')
           return redirect(url_for('add_author'))
       # Convert date strings to datetime.date objects
       birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
       death_date = datetime.strptime(death_date_str, '%Y-%m-%d').date() if death_date_str else None

       # Create a new Author instance
       new_author = Author(name=name, birth_date=birth_date, death_date=death_date)

       # Add the new author to the database
       db.session.add(new_author)
       db.session.commit()

       # Display a success message
       flash('Author added successfully!', 'success')

       return redirect(url_for('add_author'))

    return render_template('add_author.html')

@app.route("/", methods=["GET"])
def home_page():
    # Get the sorting criteria from the query parameter (default is 'title')
    sort_by = request.args.get('sort', 'title')
    # Get the search query from the form, if any
    search_query = request.args.get('search', '')



    if search_query:
        books = Book.query.join(Author).filter(
            Book.title.ilike(f'%{search_query}%') |Author.name.ilike(f'%{search_query}%')
        ).all()
    elif sort_by :
       if sort_by == 'author':
          # Sort books by author's name
          books = Book.query.join(Author).order_by(Author.name).all()
       else:
          # Default: Sort books by title
          books = Book.query.order_by(Book.title).all()



    book_data = []
    for book in books:
        cover_image = None
        if book.isbn:
            # Fetch the book cover image using the Open Library Covers API
            cover_image = f"https://covers.openlibrary.org/b/isbn/{book.isbn}-L.jpg"
        book_data.append({
            "id":book.id,
            "title": book.title,
            "author": book.author.name,  # Access the associated author's name
            "publication_year": book.publication_year,
            "isbn": book.isbn,
            "cover_image": cover_image
        })

        # Render the home page template
    return render_template("home.html", books=book_data)


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    # Get the book by its ID
    book_to_delete = Book.query.get_or_404(book_id)

    try:
        # Check if the author has any other books
        author = book_to_delete.author
        db.session.delete(book_to_delete)

        # Check if the author has any other books left
        if not author.books:
            db.session.delete(author)

        # Commit changes to the database
        db.session.commit()

        # Flash success message
        flash("Book deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting book: {str(e)}", "danger")

    # Redirect back to the homepage
    return redirect("/")
@app.route("/add_book", methods= ['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        isbn = request.form.get('isbn').strip()
        publication_year = int(request.form.get('publication_year'))
        author_id = request.form.get('author_id')  # The selected author ID
        author = Author.query.get(author_id)
        print("needed:::",author)
        # Create a new book instance
        new_book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=author_id
        )
        # Check if the author exists
        author = Author.query.get(author_id)
        if author is None:
            flash('Invalid author selected!', 'danger')
            return redirect(url_for('add_book'))
        try:
            # Add the new book to the database
            db.session.add(new_book)
            db.session.commit()

            # Flash success message
            flash("Book added successfully!", 'success')
            return redirect(url_for('add_book'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding book: {str(e)}", 'danger')

    authors = Author.query.all()
    print(authors)
    return render_template('add_book.html', authors = authors)


"""with app.app_context():
  db.create_all()"""

if __name__ == '__main__':
    app.run(debug=True)