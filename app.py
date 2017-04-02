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

    def set_title(self, title):
        self.title = title

    def get_preview(self):
        return self.preview

    def set_preview(self, body):
        self.preview = body[:300]

    def get_body(self):
        return self.body

    def set_body(self, body):
        self.body = body

    def get_creation_date(self):
        return self.creation_date

    def set_creation_date(self, creation_date=datetime.now()):
        self.creation_date = creation_date

    def get_modification_date(self):
        return self.modification_date

    def set_modification_date(self, modification_date):
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



@app.route('/', methods=['GET', 'POST'])
def new_note():
    my_form = NotesForm()
    notes = Note.query.order_by(Note.creation_date.desc()).all()
    return render_template('new_note.html', my_form=my_form, notes=notes)

@app.route('/<int:note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    my_form = NotesForm()
    notes = Note.query.order_by(Note.creation_date.desc()).all()
    single_note = Note.query.get_or_404(note_id)
    my_form.note_body.data = single_note.body
    return render_template('view_note.html', my_form=my_form, notes=notes, single_note=single_note)

if __name__ == "__main__":
    app.run()
