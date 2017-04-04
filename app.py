from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateTimeLocalField
import re
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydb.db"
app.config['DEBUG'] = None
app.config['SECRET_KEY'] = "\xf6Hs\xbe\xd5C'\xde\x88\x8e$\xbc\xfb\xc69m\xd1!\x06\x15\xa0\xc9:\x85\x17\x99\xf1\xfc0\x96\xc8\xbfp\r\x1b`>\x08\xd3\xd6"


TAG_REMOVE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_REMOVE.sub('', text)

class Note(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    preview = db.Column(db.String())
    body = db.Column(db.String())
    creation_date = db.Column(db.DateTime())
    modification_date = db.Column(db.DateTime())

    def get_title(self):
        return self.title

    def set_title(self, form):
        self.title = form.title.data

    def get_preview(self):
        return self.preview

    def set_preview(self, form):
        self.preview = form.note_body.data[:300]

    def get_body(self):
        return self.body

    def set_body(self, form):
        self.body = form.note_body.data

    def get_creation_date(self):
        time = []
        time.append(self.creation_date.strftime('%Y-%m-%d %H:%M').replace(' ', 'T'))
        return time

    def set_creation_date(self, form):
        time = form.creation_date.raw_data[0].replace('T', ' ')
        self.creation_date = datetime.strptime(time, '%Y-%m-%d %H:%M')

    def get_modification_date(self):
        time = []
        time.append(self.modification_date.strftime('%Y-%m-%d %H:%M').replace(' ', 'T'))
        return time

    def set_modification_date(self):
        self.modification_date = datetime.now()

    def __repr__(self):
        return "<Note {}>".format(self.title)

class NotesForm(FlaskForm):
    title = StringField()
    note_body = TextAreaField()
    creation_date = DateTimeLocalField()
    modification_date = DateTimeLocalField()
    new = SubmitField()
    save = SubmitField()
    delete = SubmitField()

def notes_into_db(single_note, form):
    single_note.set_title(form)
    single_note.set_preview(form)
    single_note.set_body(form)
    single_note.set_creation_date(form)
    single_note.set_modification_date()

def current_time():
    time = []
    time.append(datetime.now().strftime('%Y-%m-%d %H:%M').replace(' ', 'T'))
    return time

@app.route('/', methods=['GET', 'POST'])
def new_note():
    my_form = NotesForm()
    if(my_form.new.data):
        return redirect('/')
    if(my_form.save.data):
        single_note = Note()
        notes_into_db(single_note, my_form)
        db.session.add(single_note)
        db.session.commit()
    if(my_form.delete.data):
        return redirect('/')
    my_form.creation_date.raw_data = current_time()
    my_form.modification_date.raw_data = current_time()
    notes = Note.query.order_by(Note.creation_date.desc()).all()
    return render_template('new_note.html', my_form=my_form, notes=notes)

@app.route('/<int:note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    my_form = NotesForm()
    single_note = Note.query.get_or_404(note_id)
    if(my_form.new.data):
        return redirect('/')
    if(my_form.save.data):
        notes_into_db(single_note, my_form)
        db.session.commit()
    if(my_form.delete.data):
        db.session.delete(single_note)
        db.session.commit()
        return redirect('/')
    my_form.title.data = single_note.get_title()
    my_form.note_body.data = single_note.get_body()
    my_form.creation_date.raw_data = single_note.get_creation_date()
    my_form.modification_date.raw_data = single_note.get_modification_date()
    notes = Note.query.order_by(Note.creation_date.desc()).all()
    return render_template('view_note.html', my_form=my_form, notes=notes, single_note=single_note)

if __name__ == "__main__":
    app.run()
