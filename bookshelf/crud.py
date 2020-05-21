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

from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for, flash
from bookshelf.forms import BookSearchForm


crud = Blueprint('crud', __name__)

# [START list]
@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)
# [END list]

# Helper function
import re
def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    #text = re.sub('\W', ' ', text)
    #text = re.sub('\s+', ' ', text)
    text = text.strip(' ')
    return text

@crud.route('/init')
def init():
    # import pandas as pd
    # movies = pd.read_csv('wiki_movie_plots_deduped.csv', delimiter=',',nrows=300)
    # movies['PlotClean'] = movies['Plot'].apply(clean_text)
    # for index, row in movies.iterrows():
    #    data = {'title':row['Title'], 'author':row['Director'], 'publishedDate':row['Release Year'], 'description':row['PlotClean']}
    #     get_model().create(data)
    return redirect(url_for('.list'))


@crud.route('/<id>')
def view(id):
    book = get_model().read(id)
    return render_template("view.html", book=book)


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        print(data)
        book = get_model().create(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        book = get_model().update(data, id)
        return redirect(url_for('.view', id=book['id']))
    return render_template("form.html", action="Edit", book=book)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))

@crud.route('/<id>/rate', methods=['GET','POST'])
def rate(id):
    book = get_model().read(id)
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        book = get_model().update(data,id)
        return redirect(url_for('.view', id=book['id']))
    return render_template("rate.html", action="Edit", book=book)


@crud.route('/search', methods=['GET','POST'])
def index():
    search = BookSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)


@crud.route('/deleteall')
def deleteall():
    get_model().delete_all()
    return redirect(url_for('.list'))

@crud.route('/search/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    select_string = search.data['select']
    if select_string == 'title':
        qry = get_model().Book.query.filter(get_model().Book.title.like('%'+search_string+'%'))
        results = qry.all()
    elif select_string == 'publishedDate':
        qry = get_model().Book.query.filter(get_model().Book.publishedDate.like('%'+search_string+'%'))
        results = qry.all()
    elif select_string == 'author':
        qry = get_model().Book.query.filter(get_model().Book.author.like('%'+search_string+'%'))
        results = qry.all()
    else:
        flash('Something is definitely wrong...')
        return redirect('/books/search')
    if search_string == '':
        qry = get_model().Book.query
        results = qry.all()
        
    if not results:
        flash('No results found!')
        return redirect('/books/search')
    else:
        # display results
        return render_template('results.html', query = search_string, results=results)
