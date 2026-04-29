import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import sqlite3
import cv2

# -----------------------
# Setup
# -----------------------

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
HEATMAP_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(HEATMAP_FOLDER, exist_ok=True)

# -----------------------
# Load Model
# -----------------------

model_path = os.path.join(os.path.dirname(__file__), "Models", "knee_oa_model_final.h5")
model = tf.keras.models.load_model(model_path, compile=False)

print("✅ Model loaded successfully")

# -----------------------
# Labels
# -----------------------

labels = ["Normal", "Doubtful", "Mild", "Moderate", "Severe"]

grade_info = {
    0: "Normal – No signs of osteoarthritis",
    1: "Doubtful – Minor joint changes",
    2: "Mild – Small osteophytes detected",
    3: "Moderate – Joint space narrowing present",
    4: "Severe – Bone deformation and major narrowing"
}

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
# Grad-CAM FUNCTION
# -----------------------

def generate_gradcam(model, img_array, last_conv_layer_name="top_conv"):
    
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        class_index = tf.argmax(predictions[0])
        loss = predictions[:, class_index]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0,1,2))

    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / tf.reduce_max(heatmap)
    return heatmap.numpy()

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

    # -----------------------
    # Preprocess (FIXED)
    # -----------------------

    from tensorflow.keras.applications.efficientnet import preprocess_input

    img = Image.open(filepath).convert("RGB").resize((224, 224))
    img_array = np.array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    # -----------------------
    # Prediction
    # -----------------------

    prediction = model.predict(img_array)
    class_idx = int(np.argmax(prediction))
    confidence = float(np.max(prediction)) * 100

    result = labels[class_idx]
    explanation = grade_info[class_idx]

    print("Prediction:", result, "| Confidence:", confidence)

    # -----------------------
    # Grad-CAM
    # -----------------------

    heatmap = generate_gradcam(model, img_array)

    original = cv2.imread(filepath)
    original = cv2.resize(original, (224,224))

    heatmap = cv2.resize(heatmap, (224,224))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    superimposed_img = cv2.addWeighted(original, 0.6, heatmap, 0.4, 0)

    heatmap_filename = "heatmap_" + file.filename
    heatmap_path = os.path.join(HEATMAP_FOLDER, heatmap_filename)

    cv2.imwrite(heatmap_path, superimposed_img)

    # -----------------------
    # Save to DB
    # -----------------------

    conn = sqlite3.connect("database.db")
    conn.execute(
        "INSERT INTO patients(name, age, image, grade) VALUES (?,?,?,?)",
        (name, age, filepath, result)
    )
    conn.commit()
    conn.close()

    # -----------------------
    # Response
    # -----------------------

    return jsonify({
        "name": name,
        "age": age,
        "grade": result,
        "confidence": round(confidence, 2),
        "explanation": explanation,
        "heatmap": heatmap_path
    })

# -----------------------
# Get all patients
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