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
import time

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
    director = db.Column(db.String(255))
    releasedDate = db.Column(db.String(255))
    imageUrl = db.Column(db.String(255))
    description = db.Column(db.String(4096))
    addedDate = db.Column(db.Integer)
    rating = db.Column(db.Float, nullable = True)

    def __repr__(self):
        return "<Book(title='%s', director=%s, rating=%d)" % (self.title, self.director, self.rating)
# [END model]


# [START list]
def list(limit=10, cursor=None, sortKey="title"):
    cursor = int(cursor) if cursor else 0
    query = None
    if sortKey == 'title':
        query = (Book.query
                .order_by(Book.title)
                .limit(limit)
                .offset(cursor))
    elif sortKey == 'releasedDate-ASC':
        query = (Book.query
                .order_by(Book.releasedDate)
                .limit(limit)
                .offset(cursor))
    elif sortKey == 'releasedDate-DESC':
        query = (Book.query
                .order_by(Book.releasedDate.desc())
                .limit(limit)
                .offset(cursor))
    elif sortKey == 'addedDate-ASC':
        query = (Book.query
                .order_by(Book.addedDate)
                .limit(limit)
                .offset(cursor))
    elif sortKey == 'addedDate-DESC':
        query = (Book.query
                .order_by(Book.addedDate.desc())
                .limit(limit)
                .offset(cursor))
    else:
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
    data['addedDate'] = int(time.time())
    # print(data['addedDate'])
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return from_sql(book)
# [END create]


# [START update]
def update(data, id):
    book = Book.query.get(id)
    data['addedDate'] = int(time.time())
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

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    application = Flask(__name__)
    application.config.from_pyfile('../config.py')
    init_app(application)
    with application.app_context():
        # Hella dangerous
        # db.drop_all()
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
