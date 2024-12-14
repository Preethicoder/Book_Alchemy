from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = "authors"

    # Define attributes with appropriate types and constraints
    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    death_date = db.Column(db.Date)


    # This will create a relationship with the Book model
    books = db.relationship('Book', backref='author', lazy=True)
    # Optional: Custom string representation
    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}', birth_date={self.birth_date}, date_of_death={self.birth_date})>"

    def __str__(self):
        return f"{self.name} (Born: {self.birth_date}{' - Died: ' + str(self.death_date) if self.death_date else ''})"

class Book(db.Model):
    __tablename__ = "books"

    # Define attributes with appropriate types and constraints
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), unique=True,)
    title = db.Column(db.String(200))
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    # Optional: Custom string representation
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', isbn='{self.isbn}', publication_year={self.publication_year}, author_id={self.author_id})>"

    def __str__(self):
        return f"'{self.title}' by {self.author.name} (Published: {self.publication_year})"




