'''Import SQLALchemy for database/model'''
from flask_sqlalchemy import SQLAlchemy
'''Regular expression to remove html tags from a text'''
import re
'''To store/retrieve datetime in/from database'''
from datetime import datetime


'''sqlalchemy database object'''
db = SQLAlchemy()

'''remove all html tag from a text'''
def remove_tags(text):
    TAG_REMOVE = re.compile(r'<[^>]+>')
    return TAG_REMOVE.sub('', text)

'''returns current time in a list, in a formatted way
which can be used in the wtform'''
def current_time():
    time = []
    time.append(datetime.now().strftime('%Y-%m-%d %H:%M').replace(' ', 'T'))
    return time

'''sqlalchemy model for notebooks'''
class Notebook(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    sections = db.relationship('Section', backref='notebook', lazy='dynamic')

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def __repr__(self):
        return "<Notebook {}>".format(self.title)

'''sqlalchemy model for sections'''
class Section(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    notes = db.relationship('Note', backref='section', lazy='dynamic')
    notebook_id = db.Column(db.Integer(), db.ForeignKey('notebook.id'))

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_notebook_id(self):
        return self.notebook_id

    def __repr__(self):
        return "<Section {}>".format(self.title)

'''sqlalchemy model to represent database table'''
class Note(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    preview = db.Column(db.String())
    body = db.Column(db.String())
    creation_date = db.Column(db.DateTime())
    modification_date = db.Column(db.DateTime())
    section_id = db.Column(db.Integer(), db.ForeignKey('section.id'))

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_preview(self):
        return self.preview

    '''takes form object
    then takes the note_body and removes all html tags
    stores first 300 character'''
    def set_preview(self, form):
        preview = remove_tags(form.note_body.data)
        self.preview = preview[:300]

    def get_body(self):
        return self.body

    def set_body(self, form):
        self.body = form.note_body.data

    '''wtform datetime only accepts a list
    containing only 1 item in a specific format
    so we get the time from database, format it accordingly
    the use this function to display in the browser'''
    def get_creation_date(self):
        time = []
        time.append(self.creation_date.strftime('%Y-%m-%d %H:%M').replace(' ', 'T'))
        return time

    '''wtform datetime returns datetime like a normal datetime form field, in a list
    using raw_data we are getting the list
    and formatting that accordingly to store in database'''
    def set_creation_date(self, form):
        time = form.creation_date.raw_data[0].replace('T', ' ')
        self.creation_date = datetime.strptime(time, '%Y-%m-%d %H:%M')

    '''wtform datetime only accepts a list
    containing only 1 item in a specific format
    so we get the time from database, format it accordingly
    the use this function to display in the browser'''
    def get_modification_date(self):
        time = []
        time.append(self.modification_date.strftime('%Y-%m-%d %H:%M').replace(' ', 'T'))
        return time

    '''current saving time will be set as modification date
    and users cant change it.'''
    def set_modification_date(self):
        self.modification_date = datetime.now()

    def get_section_id(self):
        return self.section_id

    def __repr__(self):
        return "<Note {}>".format(self.title)
