# Import flask objects
from flask import Flask, render_template, request, url_for, redirect
# Import SQLALchemy for database/model
from flask_sqlalchemy import SQLAlchemy
# Get the user inputs using flask-wtf instead of directly using html form objects.
# HTML5 datetime field provides a calender to easily choose date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateTimeLocalField
# Regular expression to remove html tags from a text
import re
# To store/retrieve datetime in/from database
from datetime import datetime

# flask app object
app = Flask(__name__)

# sqlalchemy database object
db = SQLAlchemy(app)

# location of the database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydb.db"

# debug mode on for developement environment
app.config['DEBUG'] = None

# for session and cookies
app.config['SECRET_KEY'] = "\xf6Hs\xbe\xd5C'\xde\x88\x8e$\xbc\xfb\xc69m\xd1!\x06\x15\xa0\xc9:\x85\x17\x99\xf1\xfc0\x96\xc8\xbfp\r\x1b`>\x08\xd3\xd6"

# remove all html tag from a text
TAG_REMOVE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_REMOVE.sub('', text)

# sqlalchemy model to represent database table
class Note(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    preview = db.Column(db.String())
    body = db.Column(db.String())
    creation_date = db.Column(db.DateTime())
    modification_date = db.Column(db.DateTime())

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_preview(self):
        return self.preview

    # takes form object
    # then takes the note_body and removes all html tags
    # stores first 300 character
    def set_preview(self, form):
        preview = remove_tags(form.note_body.data)
        self.preview = preview[:300]

    def get_body(self):
        return self.body

    def set_body(self, form):
        self.body = form.note_body.data

    # wtform datetime only accepts a list
    # containing only 1 item in a specific format
    # so we get the time from database, format it accordingly
    # the use this function to display in the browser
    def get_creation_date(self):
        time = []
        time.append(self.creation_date.strftime('%Y-%m-%d %H:%M').replace(' ', 'T'))
        return time

    # wtform datetime returns datetime like a normal datetime form field, in a list
    # using raw_data we are getting the list
    # and formatting that accordingly to store in database
    def set_creation_date(self, form):
        time = form.creation_date.raw_data[0].replace('T', ' ')
        self.creation_date = datetime.strptime(time, '%Y-%m-%d %H:%M')

    # wtform datetime only accepts a list
    # containing only 1 item in a specific format
    # so we get the time from database, format it accordingly
    # the use this function to display in the browser
    def get_modification_date(self):
        time = []
        time.append(self.modification_date.strftime('%Y-%m-%d %H:%M').replace(' ', 'T'))
        return time

    # current saving time will be set as modification date
    # and users cant change it.
    def set_modification_date(self):
        self.modification_date = datetime.now()

    def __repr__(self):
        return "<Note {}>".format(self.title)

# using flask-wtf to create a form class 
class NotesForm(FlaskForm):
    title = StringField()
    note_body = TextAreaField()
    creation_date = DateTimeLocalField()
    modification_date = DateTimeLocalField()
    new = SubmitField()
    save = SubmitField()
    delete = SubmitField()

# takes note object/instance and form object as parameter
# then sends all data in the database,
# not stage or commit, only prepares
# returns true if its an empty note
def notes_into_db(single_note, form):
    single_note.set_title(form.title.data)
    single_note.set_preview(form)
    single_note.set_body(form)
    single_note.set_creation_date(form)
    single_note.set_modification_date()
    # if title is not set when saving
    # then takes first 100 char from preview
    # from preview, vause tags are already removed
    if(single_note.get_title() == ''):
        title = single_note.get_preview()
        single_note.set_title(title[:100])
    # if both title and body is empty, means empty note
    # returns true so, empty note wont be saved.
    if((single_note.get_title() == '') and (single_note.get_body() == '')):
        return True

# returns current time in a list, in a formatted way
# which can be used in the wtform
def current_time():
    time = []
    time.append(datetime.now().strftime('%Y-%m-%d %H:%M').replace(' ', 'T'))
    return time

# this function creates a new note
@app.route('/', methods=['GET', 'POST'])
def new_note():
    # define a new form object/instance
    my_form = NotesForm()
    # if new button is pressed refresh page
    if(my_form.new.data):
        return redirect('/')
    # if save button is pressed, create a Note() model/instance
    # use notes_into_db to send all data into the database
    # if both title and body is empty, then do nothing
    # else, stage all changes in the database and
    # finally write this new note in the database
    # after writing into database, load this new note from database.
    if(my_form.save.data):
        single_note = Note()
        empty = notes_into_db(single_note, my_form)
        if(empty):
            return redirect('/')
        db.session.add(single_note)
        db.session.commit()
        return redirect(url_for('view_note', note_id = single_note.get_id()))
    # if delete button is pressed, refresh page
    if(my_form.delete.data):
        return redirect('/')
    # when writing a new note, always set the creation date
    # and modification date to current time
    # btw creation date can be changed, but modification date can't be changed
    my_form.creation_date.raw_data = current_time()
    my_form.modification_date.raw_data = current_time()
    # get all notes from database in a descending order
    notes = Note.query.order_by(Note.creation_date.desc()).all()
    # normally render the new note page
    # and pass the form object and all notes from database
    return render_template('new_note.html', my_form=my_form, notes=notes)

# this function displays a note from database
# when the address gets a note_id/primary key of a note
# it displays that note.
@app.route('/<int:note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    # define a new form object
    my_form = NotesForm()
    # loads/selects a row based on note_id
    # if note_id is not available then automatically return 404 error
    single_note = Note.query.get_or_404(note_id)
    # if new button is pressed, discard all changes, go to new note page
    if(my_form.new.data):
        return redirect('/')
    # if save button is pressed, save all modifications using notes_into_db function
    if(my_form.save.data):
        empty = notes_into_db(single_note, my_form)
        if(empty):
            return redirect('/')
        db.session.commit()
    # if delete button is pressed, select this column
    # delete the column, and commit this delete in database
    # and return to create new note page
    if(my_form.delete.data):
        db.session.delete(single_note)
        db.session.commit()
        return redirect('/')
    # load note title, body, creation and modification date from database
    # into the form object, so when rendering, this datas will be automatically loaded
    # this could be also done from template
    # but all logics only in the backend is more efficient
    my_form.title.data = single_note.get_title()
    my_form.note_body.data = single_note.get_body()
    my_form.creation_date.raw_data = single_note.get_creation_date()
    my_form.modification_date.raw_data = single_note.get_modification_date()
    # get all notes from database in a descending order
    notes = Note.query.order_by(Note.creation_date.desc()).all()
    # rendering note from database
    return render_template('view_note.html', my_form=my_form, notes=notes, single_note=single_note)

# File manager----------------------------
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'static/media/'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'bmp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            funcNum = request.args.get('CKEditorFuncNum')
            fileUrl = 'static/' + filename
            print(fileUrl)
            return render_template('file_browser.html', close_window=True, funcNum=funcNum, fileUrl=fileUrl)

    return render_template('file_browser.html')
#----------------------------------------------

if __name__ == "__main__":
    app.run()
