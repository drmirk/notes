'''Get the user inputs using flask-wtf instead of directly using html form objects.
HTML5 datetime field provides a calender to easily choose date'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateTimeLocalField

class NotesForm(FlaskForm):
    '''using flask-wtf to create a
    form class for notes'''
    title = StringField()
    note_body = TextAreaField()
    creation_date = DateTimeLocalField()
    modification_date = DateTimeLocalField()
    new = SubmitField()
    save = SubmitField()
    delete = SubmitField()

class NotebookForm(FlaskForm):
    '''using flask-wtf to create a
    form class for notebooks'''
    current_title = StringField()
    new_title = StringField()
    new = SubmitField()
    save = SubmitField()
    delete = SubmitField()
