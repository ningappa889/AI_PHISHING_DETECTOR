# 🛡️ AI Phishing URL Detection System

An AI-powered phishing URL detection system built using **Python**, **Machine Learning**, and **Flask**. The application analyzes URLs and predicts whether they are **Safe** or **Phishing** using a trained machine learning model.

---

## 📌 Features

- 🔍 Detects phishing URLs
- 🤖 Machine Learning based prediction
- 📊 Trained on 650,000+ URLs
- 📈 Uses TF-IDF vectorization
- ⚡ Logistic Regression classifier
- 🌐 Flask web application (Coming Soon)
- 💾 Saved trained model using Joblib

---

## 🛠️ Technologies Used

- Python 3.13
- Pandas
- NumPy
- Scikit-learn
- Flask
- Joblib
- Matplotlib
- Git & GitHub

---

## 📂 Project Structure

```
AI_PHISHING_DETECTION/
│
├── dataset/
│   ├── malicious_phish.csv
│   └── cleaned_dataset.csv
│
├── model/
│   ├── phishing_model.pkl
│   └── vectorizer.pkl
│
├── static/
├── templates/
├── tests/
├── utils/
│
├── app.py
├── explore_dataset.py
├── preprocess_dataset.py
├── train_model.py
├── predict.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 📊 Dataset

- Total URLs: **651,191**
- Classes:
  - Benign
  - Phishing
  - Malware
  - Defacement

After preprocessing:

- **Safe (0)** → Benign
- **Malicious (1)** → Phishing + Malware + Defacement

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/AI_PHISHING_DETECTION.git
```

Move into the project:

```bash
cd AI_PHISHING_DETECTION
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Explore the dataset

```bash
python explore_dataset.py
```

### Preprocess the dataset

```bash
python preprocess_dataset.py
```

### Train the model

```bash
python train_model.py
```

### Test the model

```bash
python predict.py
```

### Run the Flask application (Coming Soon)

```bash
python app.py
```

---

## 📈 Model Performance

Current Model:

- Logistic Regression
- TF-IDF Vectorization

Accuracy:

**94.99%**

> Future versions will compare multiple machine learning models to improve detection performance.

---

## 🚀 Future Improvements

- Character-level TF-IDF
- Compare multiple ML models
- Flask Web Interface
- Explainable AI predictions
- Browser Extension
- REST API
- Docker support
- Cloud Deployment

---

## 👨‍💻 Author

**Ningappa**

Computer Science & Engineering Student

Interested in:
- Cybersecurity
- Machine Learning
- Artificial Intelligence
- Python Development

---

## 📄 License

This project is licensed under the MIT License.
