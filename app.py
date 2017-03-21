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

@app.route('/', methods=['GET', 'POST'])
def home():
    if(request.method == "POST"):
        if(request.form['submit'] == "New"):
            return redirect('/')
        if(request.form['submit'] == "Save"):
            if((request.form['title'] == '') and (request.form['editor1'] == '')):
                return redirect('/')
            single_note = Note()
            single_note.title = request.form['title']
            single_note.body = request.form['editor1']
            preview = remove_tags(single_note.body)
            single_note.preview = preview[:300]
            if(request.form['title'] == ''):
                single_note.title = preview[:100]
            creation_time = request.form['creation_date'].replace('T', ' ')
            single_note.creation_date = datetime.strptime(creation_time, '%Y-%m-%d %H:%M')
            modification_time = request.form['modification_date'].replace('T', ' ')
            single_note.modification_date = datetime.strptime(modification_time, '%Y-%m-%d %H:%M')
            db.session.add(single_note)
            db.session.commit()
    notes = Note.query.all()
    time = datetime.now().strftime('%Y-%m-%d %H:%M').replace(' ', 'T')
    return render_template('home.html', notes=notes, time=time)

@app.route('/<int:note_id>', methods=['GET', 'POST'])
def home2(note_id):
    if(request.method == "POST"):
        if(request.form['submit'] == "New"):
            return redirect('/')
        if(request.form['submit'] == "Save"):
            single_note = Note.query.get(note_id)
            single_note.title = request.form['title']
            single_note.body = request.form['editor1']
            preview = remove_tags(single_note.body)
            if(len(preview) >= 300):
                single_note.preview = preview[:300]
            else:
                single_note.preview = preview
            creation_time = request.form['creation_date'].replace('T', ' ')
            single_note.creation_date = datetime.strptime(creation_time, '%Y-%m-%d %H:%M')
            modification_time = request.form['modification_date'].replace('T', ' ')
            single_note.modification_date = datetime.strptime(modification_time, '%Y-%m-%d %H:%M')
            db.session.commit()
        if(request.form['submit'] == "Delete"):
            single_note = Note.query.get_or_404(note_id)
            db.session.delete(single_note)
            db.session.commit()
            return redirect('/')
    notes = Note.query.all()
    single_note = Note.query.get_or_404(note_id)
    time = datetime.now().strftime('%Y-%m-%d %H:%M').replace(' ', 'T')
    return render_template('home2.html', notes=notes, single_note=single_note, time=time)

if __name__ == "__main__":
    app.run()
