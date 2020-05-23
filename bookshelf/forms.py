from wtforms import Form, StringField, SelectField

class BookSearchForm(Form):
    choices = [('title', 'Title'),
               ('releasedDate', 'Year'),
               ('director','Director')]
    select = SelectField('Search for movies:', choices=choices)
    search = StringField('')


class BookSortingForm(Form):
    choices = [('title', 'Title'),
               ('releasedDate-DESC', 'Year (newest to oldest)'),
               ('releasedDate-ASC','Year (oldest to newest)'),
               ('addedDate-DESC', 'Added Date (most recent to oldest)'),
               ('addedDate-ASC', 'Added Date (oldest to most recent)')]
    select = SelectField('Sort movies by :', choices=choices)
