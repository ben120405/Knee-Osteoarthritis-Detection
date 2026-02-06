import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import sqlite3

# -----------------------
# Setup
# -----------------------

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------
# Load Model (SAFE PATH)
# -----------------------

model_path = os.path.join(os.path.dirname(__file__), "AlexNet_KL_Classifier.h5")
model = tf.keras.models.load_model(model_path)

print("✅ Model loaded successfully")


# -----------------------
# Database Init
# -----------------------

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


# -----------------------
# Routes
# -----------------------

@app.route("/")
def home():
    return "Backend Running 🚀"


# -----------------------
# Prediction Route
# -----------------------

@app.route("/predict", methods=["POST"])
def predict():

    print(">>> Predict route called")

    file = request.files['image']
    name = request.form['name']
    age = request.form['age']

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Preprocess image
    SIZE = 227
    img = Image.open(filepath).convert("RGB").resize((227, 227))
    img = np.array(img).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    # Prediction
    prediction = model.predict(img)
    print("Prediction:", prediction)
    grade = int(np.argmax(prediction))

    print("Sending response:", grade)
    print("Prediction:", grade)

    # Save to DB
    conn = sqlite3.connect("database.db")
    conn.execute(
        "INSERT INTO patients(name, age, image, grade) VALUES (?,?,?,?)",
        (name, age, filepath, grade)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "name": name,
        "age": age,
        "grade": grade
    })


# -----------------------
# Get all patients (optional)
# -----------------------

@app.route("/patients")
def get_patients():
    conn = sqlite3.connect("database.db")
    data = conn.execute("SELECT * FROM patients").fetchall()
    conn.close()

    return jsonify(data)


# -----------------------

if __name__ == "__main__":
    app.run(debug=True)
