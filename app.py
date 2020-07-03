import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'note_page'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tAdm1n@myfirstcluster-kojuu.mongodb.net/note_page?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_notes')
def get_notes():
    return render_template("notes.html", notes=mongo.db.notes.find())

@app.route('/add_note')
def add_note():
    return render_template("addnote.html")

@app.route('/insert_note')
def insert_note():
    notes = mongo.db.notes
    notes.insert_one(request.form.to_dict())
    return redirect(url_for('get_notes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)