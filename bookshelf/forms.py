from wtforms import Form, StringField, SelectField

class BookSearchForm(Form):
    choices = [('title', 'Title'),
               ('publishedDate', 'Year'),
               ('author','Author')]
    select = SelectField('Search for books:', choices=choices)
    search = StringField('')
