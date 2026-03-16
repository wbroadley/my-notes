from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

app = Flask(__name__)

# Tell Flask where to put the database file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html")

# Define a "Note" table as a Python class
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)

# Create the table if it doesn't exist
with app.app_context():
    db.create_all()

# --- Routes ---

# GET all notes
@app.route("/notes", methods=["GET"])
def get_notes():
    notes = Note.query.all()
    return jsonify([{"id": n.id, "content": n.content} for n in notes])

# POST a new note
@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    new_note = Note(content=data["content"])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"id": new_note.id, "content": new_note.content}), 201

# DELETE a note
@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    app.run(debug=True)