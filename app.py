from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydb.db"
app.config['DEBUG'] = None


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

    def __repr__(self):
        return "<Note {}>".format(self.title)


def form_in_db(single_note):
    single_note.title = request.form['title']
    single_note.body = request.form['editor1']
    preview = remove_tags(single_note.body)
    single_note.preview = preview[:300]
    if(single_note.title == ''):
        single_note.title = preview[:100]
    creation_time = request.form['creation_date'].replace('T', ' ')
    single_note.creation_date = datetime.strptime(creation_time, '%Y-%m-%d %H:%M')
    single_note.modification_date = datetime.now()
    if((single_note.title == '') and (single_note.body == '')):
        return True


@app.route('/', methods=['GET', 'POST'])
def new_note():
    if(request.method == "POST"):
        if(request.form['submit'] == "New"):
            return redirect('/')
        if(request.form['submit'] == "Save"):
            single_note = Note()
            empty = form_in_db(single_note)
            if(empty):
                return redirect('/')
            db.session.add(single_note)
            db.session.commit()
    notes = Note.query.order_by(Note.creation_date.desc()).all()
    time = datetime.now().strftime('%Y-%m-%d %H:%M').replace(' ', 'T')
    return render_template('new_note.html', notes=notes, time=time)

@app.route('/<int:note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    if(request.method == "POST"):
        if(request.form['submit'] == "New"):
            return redirect('/')
        if(request.form['submit'] == "Save"):
            single_note = Note.query.get(note_id)
            empty = form_in_db(single_note)
            if(empty):
                return redirect('/')
            db.session.commit()
        if(request.form['submit'] == "Delete"):
            single_note = Note.query.get_or_404(note_id)
            db.session.delete(single_note)
            db.session.commit()
            return redirect('/')
    notes = Note.query.order_by(Note.creation_date.desc()).all()
    time = datetime.now().strftime('%Y-%m-%d %H:%M').replace(' ', 'T')
    single_note = Note.query.get_or_404(note_id)
    return render_template('view_note.html', notes=notes, single_note=single_note, time=time)

if __name__ == "__main__":
    app.run()
