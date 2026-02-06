# Knee Osteoarthritis Detection using Deep Learning

A full-stack web application that detects **Knee Osteoarthritis (OA) grade** from X-ray images using a **pre-trained AlexNet CNN model**, with a modern dashboard interface for doctors and patient data management.

## Project Overview

Knee Osteoarthritis is a degenerative joint disease that affects millions worldwide. Early diagnosis helps slow progression and improve treatment outcomes.  
This project applies Deep Learning and Computer Vision to automatically classify knee X-ray images into Kellgren–Lawrence (KL) grades (0–4).

The system combines:
- AI-powered medical image analysis
- A clean web dashboard
- Patient history storage
- Visual analytics

---

## Key Features

-  **Deep Learning Model**
  - AlexNet CNN trained on knee X-ray dataset
  - Predicts KL Grades from 0 (Normal) to 4 (Severe OA)

- **Full-Stack Web Application**
  - Flask backend REST API
  - HTML, CSS, JavaScript frontend

-  **Interactive Dashboard**
  - Upload knee X-ray images
  - Instant OA grade prediction
  - Patient history table
  - Grade distribution chart
  - Doctors information panel

-  **Database Integration**
  - Stores patient name, age, prediction grade, and image path
  - SQLite database used

  - **Modern UI Design**
  - SaaS-style dashboard
  - Hidden sidebar with hamburger menu
  - Icons, gradients, animations
  - Responsive layout

##  Tech Stack

🔹 Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js
- Font Awesome

🔹 Backend
- Python
- Flask
- Flask-CORS

🔹 Deep Learning
- TensorFlow / Keras
- AlexNet CNN

🔹 Database
- SQLite3


## 📂 Project Structure
knee_oa_project/
│
├── backend/
│ ├── app.py
│ ├── database.db
│ ├── uploads/
│ └── requirements.txt
│
├── frontend/
│ └── index.html
│
├── .gitignore
└── README.md


> ⚠️ **Note:**  
> The trained deep learning model file (`.h5 / .keras`) is intentionally excluded from the GitHub repository due to GitHub file size limits and industry best practices.

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ben120405/Knee-Osteoarthritis-Detection.git
cd Knee-Osteoarthritis-Detection

2️⃣ Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
3️⃣ Run Backend Server
python app.py


The backend server will start at:

http://127.0.0.1:5000

4️⃣ Run Frontend

Open the file below directly in a browser:

frontend/index.html

🧪 Model Information

Model Architecture: AlexNet CNN

Input Image Size: 227 × 227 × 3

Output Classes: KL Grades (0–4)

Dataset: Knee X-ray images

Task: Multiclass classification

The model is used only for inference in this application.

📈 Output Interpretation
KL Grade	Description
0	Normal
1	Doubtful OA
2	Mild OA
3	Moderate OA
4	Severe OA

🔒 Model & GitHub Handling:

GitHub does not allow files larger than 100 MB
Trained ML models are excluded via .gitignore
Models should be stored locally or on cloud storage
This approach follows industry-standard deployment practices

💡 Future Enhancements:

🔐 Doctor login & authentication          
☁ Cloud deployment (Render / AWS)
📱 Mobile-responsive UI
🧾 PDF & CSV report generation
📊 Advanced analytics & insights
🤖 Model optimization and retraining

👨‍💻 Author
Benin Dbritto
Engineering Student


📜 License
This project is developed for educational and research purposes.

If you found this project helpful, feel free to star the repository!


