# 🚀 Resume Builder (Streamlit + AWS + PDF Automation)

A dynamic resume builder application that allows users to create, edit, and manage multiple role-specific resumes (Data Scientist, Cloud Data Engineer, Solutions Architect) with automated PDF generation and cloud storage using AWS S3.

---

## 🔥 Features

* ✨ Interactive UI using Streamlit
* 📂 Role-based resume management (DS / CDE / SA)
* 📝 JSON-based structured resume editing
* 📄 Automated PDF generation using ReportLab
* ☁️ Upload and store resumes in AWS S3
* 🔗 Generate shareable resume links
* 🔄 Real-time updates and persistence

---

## 🏗️ Architecture Overview
```bash
Streamlit UI
     ⬇
Session State (Resume Data)
     ⬇
JSON Storage (AWS S3)
     ⬇
PDF Generator (ReportLab)
     ⬇
S3 Upload (Final Resume PDF)
```

---

## ⚙️ Tech Stack

* **Frontend/UI:** Streamlit
* **Backend Logic:** Python
* **PDF Generation:** ReportLab
* **Cloud Storage:** AWS S3 (boto3)

---

## 📸 Key Functionalities

### 1. Resume Editing

* Add/Edit:

  * Skills
  * Experience
  * Projects
  * Education
  * Certifications
* Role-specific customization

### 2. Cloud Storage

* Saves resume JSON to S3
* Loads existing data from S3

### 3. PDF Generation

* Converts structured JSON → formatted PDF
* Clean, professional layout

---

## 🚀 How to Run

### 1. Clone the repo

```bash
git clone https://github.com/your-username/resume-builder.git
cd resume-builder
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure AWS Credentials

**Option 1 (Recommended):**

```bash
aws configure
```

**Option 2: Environment Variables**

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

---

### 4. Run the app

```bash
streamlit run app.py
```

---

## ⚠️ Security Note

Do NOT hardcode AWS credentials in the code.
Always use environment variables or IAM roles.

---

## 📌 Future Improvements

* Resume versioning
* Public resume hosting page
* Multiple templates/themes
* Lambda-based automation pipeline
* Authentication system

---

## 💡 Use Case

This project demonstrates:

* Full-stack data application development
* Cloud integration (AWS S3)
* Real-world document generation pipeline

---

## 👤 Author

**Tanmay Melanta**

* LinkedIn: https://www.linkedin.com/in/tanmay-melanta/
* GitHub: https://github.com/tanmaymelanta

---

## ⭐ If you like this project, give it a star!
