from wtforms import Form, StringField, SelectField

class BookSearchForm(Form):
    choices = [('title', 'Title'),
               ('releasedDate', 'Year'),
               ('director','Director')]
    select = SelectField('Search for movies:', choices=choices)
    search = StringField('')


class BookSortingForm(Form):
    choices = [('title', 'Title'),
               ('releasedDate', 'Year'),
               ('addedDate', 'Added Date')]
    choices_order = [('DESC', 'descending order'), ('ASC', 'ascending order')]
    select = SelectField('Sort movies by :', choices=choices)
    select_choice = SelectField('', choices = choices_order)