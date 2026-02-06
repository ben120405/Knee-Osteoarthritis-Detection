import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import sqlite3

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ========================
# Load Model
# ========================
model_path = os.path.join(os.path.dirname(__file__), "AlexNet_KL_Classifier.h5")
model = tf.keras.models.load_model(model_path)

print("✅ Model loaded")


# ========================
# DB Setup
# ========================
def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            grade TEXT,
            image TEXT
        )
    """)
    conn.close()

init_db()


# ========================
@app.route("/")
def home():
    return "Backend running 🚀"


# ========================
# Predict
# ========================
@app.route("/predict", methods=["POST"])
def predict():

    file = request.files['image']
    name = request.form['name']
    age = request.form['age']

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    img = Image.open(filepath).resize((224,224))
    img = np.array(img)/255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    grade = str(np.argmax(prediction))

    conn = sqlite3.connect("database.db")
    conn.execute(
        "INSERT INTO patients(name, age, grade, image) VALUES (?,?,?,?)",
        (name, age, grade, filepath)
    )
    conn.commit()
    conn.close()

    return jsonify({"grade": grade})


# ========================
# History API
# ========================
@app.route("/patients")
def patients():

    conn = sqlite3.connect("database.db")
    rows = conn.execute("SELECT * FROM patients").fetchall()
    conn.close()

    return jsonify(rows)


# ========================
if __name__ == "__main__":
    app.run(debug=True)
