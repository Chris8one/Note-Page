import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

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

@app.route('/insert_note', methods=['POST'])
def insert_note():
    notes = mongo.db.notes
    notes.insert_one(request.form.to_dict())
    return redirect(url_for('get_notes', _anchor="notes"))

@app.route('/edit_note/<note_id>')
def edit_note(note_id):
    the_note = mongo.db.notes.find_one({"_id": ObjectId(note_id)})
    return render_template("editnote.html", note=the_note)

@app.route('/update_note/<note_id>', methods=['POST'])
def update_note(note_id):
    notes = mongo.db.notes
    notes.update({'_id': ObjectId(note_id)},
    {
        'note_title': request.form.get('note_title'),
        'note_information': request.form.get('note_information')
    })
    return redirect(url_for('get_notes', _anchor="notes"))

@app.route('/delete_note/<note_id>')
def delete_note(note_id):
    mongo.db.notes.remove({"_id": ObjectId(note_id)})
    return redirect(url_for('get_notes', _anchor="notes"))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)