# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


builtin_list = list


db = SQLAlchemy()


def init_app(application):
    # Disable track modifications, as it unnecessarily uses memory.
    application.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(application)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# [START model]
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publishedDate = db.Column(db.String(255))
    imageUrl = db.Column(db.String(255))
    description = db.Column(db.String(4096))
    createdBy = db.Column(db.String(255))
    createdById = db.Column(db.String(255))
    rating = db.Column(db.Float, nullable = True)

    def __repr__(self):
        return "<Book(title='%s', author=%s, rating=%d)" % (self.title, self.author, self.rating)
# [END model]

# class Rating(db.Model):
#     __tablename__ = 'ratings'
#     rating_id = db.Column(db.Integer,primary_key = True)
#     book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
#     rate = db.Column(db.Integer)

#     book = db.relationship("Book",backref=db.backref("ratings"), order_by=rating_id)

#     def __repr__(self):
#         return "<Rating of book %s by you is %s>" % (self.book_id, self.score)

# [START list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Book.query
             .order_by(Book.title)
             .limit(limit)
             .offset(cursor))
    books = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)
# [END list]


# [START read]
def read(id):
    result = Book.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]


# [START create]
def create(data):
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return from_sql(book)
# [END create]


# [START update]
def update(data, id):
    book = Book.query.get(id)
    for k, v in data.items():
        setattr(book, k, v)
    db.session.commit()
    return from_sql(book)
# [END update]


def delete(id):
    Book.query.filter_by(id=id).delete()
    db.session.commit()

def delete_all():
    Book.query.delete()
    db.session.commit()

# def create_rate(data):
#     rate = Rating(**data)
#     db.session.add(rate)
#     db.session.commit()
#     return from_sql(rate)

# def update_rate(data,id):
#     rate = Rating.query.get(id)
#     for k, v in rate.items():
#         setattr(rate, k, v)
#     db.session.commit()
#     return from_sql(rate)

# def read_rate(id):
#     result = Rating.query.get(id)
#     if not result:
#         return None
#     return from_sql(result)

# def delete_rate(id):
#     Rating.query.filter_by(id=id).delete()
#     db.session.commit()

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    application = Flask(__name__)
    application.config.from_pyfile('../config.py')
    init_app(application)
    with application.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
