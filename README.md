# 🛡️ PhishGuard AI – AI Phishing URL Detector

An AI-powered phishing URL detection platform and cybersecurity web application built using **Python**, **Machine Learning (Linear SVM + TF-IDF)**, and **Flask**.

PhishGuard AI analyzes URLs in real time using lexical feature extraction, structural analysis, and threat heuristics to deliver **Explainable AI (XAI)** threat verdicts and continuous 5-tier security risk scores.

---

## 📌 Features

- 🤖 **AI-Powered Detection**: Trained on 650,000+ benchmarked URLs using Linear SVM & TF-IDF NLP vectorization.
- 📐 **Structural & Lexical Analysis**: Extracts URL length, domain length, subdomains, slash counts, hyphens, and Shannon entropy.
- 📊 **Dynamic Risk Index (0–100%)**: Categorizes links into 5 risk levels (Minimal, Low, Moderate, High, Critical).
- 💡 **Explainable AI (XAI) Reasoning**: Generates interpretable bullet-point evidence explaining why a link received its score.
- 🌐 **Live Demo**: [urlsecure.vercel.app](https://urlsecure.vercel.app/) (Alternative: [aiphishguard.vercel.app](https://aiphishguard.vercel.app/))
- 🌐 **Modern Landing Page & Scanner**: Premium cybersecurity landing page at `/` and live URL scanner at `/scan`.
- ☁️ **Vercel Ready**: Pre-configured serverless setup (`vercel.json`) for zero-downtime deployment.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13, Flask
- **Machine Learning & Data**: Scikit-learn (Linear SVM), TF-IDF Vectorizer, Pandas, NumPy, Joblib
- **Frontend**: HTML5, CSS3 (Glassmorphism & CSS Variables), JavaScript ES6
- **Deployment**: Vercel Serverless Functions (`@vercel/python`), Gunicorn

---

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ningappa889/AI_PHISHING_DETECTOR.git
   cd AI_PHISHING_DETECTOR
   ```

2. **Create & activate virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application:**
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your browser.

---

## 🧪 Running Tests

Run the automated test suite:
```bash
python -m unittest discover tests
```

---

## 👨‍💻 Developer & Links

**Ningappa Hirekudi**  
*Computer Science & Engineering | AI & Cybersecurity Enthusiast*

- 📦 **GitHub Repository**: [github.com/ningappa889/AI_PHISHING_DETECTOR](https://github.com/ningappa889/AI_PHISHING_DETECTOR)
- 💻 **GitHub Profile**: [github.com/ningappa889](https://github.com/ningappa889)
- 🔗 **LinkedIn**: [linkedin.com/in/ningappa-hirekudi-892677346](https://www.linkedin.com/in/ningappa-hirekudi-892677346)
- ✉️ **Email**: [ningappahirekudi889@gmail.com](mailto:ningappahirekudi889@gmail.com)

---

## 📄 License

This project is licensed under the MIT License.
