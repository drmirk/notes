from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydb.db"
app.config['DEBUG'] = None


class Note(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    preview = db.Column(db.String())
    body = db.Column(db.String())

    def __repr__(self):
        return "<Note {}>".format(self.title)

@app.route('/')
def home():
    notes = Note.query.all()
    return render_template('home.html', notes=notes)

@app.route('/<int:note_id>')
def home2(note_id):
    notes = Note.query.all()
    single_note = Note.query.get_or_404(note_id)
    return render_template('home2.html', notes=notes, single_note=single_note)

if __name__ == "__main__":
    app.run()
