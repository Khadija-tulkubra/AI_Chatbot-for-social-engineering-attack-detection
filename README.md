# AI Chatbot for Social Engineering Attack Detection

**Author:** Khadija Tul Kubra  
**Roll #:** BITF22M025

---

## 1. Project Overview

This project is an **AI-powered Chatbot** that detects messages indicative of **Social Engineering Attacks** (e.g., phishing, smishing) in SMS or chat platforms. The system leverages **Natural Language Processing (NLP)** and a **Logistic Regression** model to classify messages as **Safe (HAM)** or **Unsafe (SPAM/Attack)**.  

It is a **Full Stack Web Application** with an interactive frontend, a high-performance backend API, and a robust ML prediction layer.

---

## 2. Problem Statement

Social engineering attacks exploit human psychology to trick users into revealing sensitive information. Manual detection is challenging due to the volume and sophisticated phrasing of these messages.  

This chatbot provides a **web-based solution** where users input messages and receive real-time classification results, enhancing awareness and protection against social engineering.

---

## 3. Technology Stack

| Component      | Technology       | Role |
|----------------|----------------|------|
| Frontend (UI)  | Next.js (React) | User interface for message input and displaying results |
| Backend/API    | FastAPI (Python)| Handles API requests and ML prediction |
| NLP & ML       | Scikit-learn    | Text preprocessing, TF-IDF vectorization, model training/prediction |
| Server         | Uvicorn         | Runs the FastAPI application locally |

---

## 4. Machine Learning Pipeline

### 4.1 Dataset
- **Source:** [Kaggle SMS Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)  
- **Labels:** 'Spam' → Unsafe/Attack, 'Ham' → Safe  
- **Preprocessing:**  
  - Text cleaning: removal of stopwords, punctuation, and special characters  
  - Label conversion for project context  

### 4.2 Data Vectorization
- **Tool:** `TfidfVectorizer` (scikit-learn)  
- **Explanation:** Converts text into numerical vectors, assigning weights to words based on importance in the dataset.

### 4.3 Model Training
- **Model:** Logistic Regression  
- **Rationale:** Efficient, fast, simple, and suitable for real-time text classification  
- **Output:** Binary prediction – 0 (Safe/HAM) or 1 (Unsafe/SPAM)

---

## 5. Project Architecture

1. **Frontend (Next.js)**: Captures user messages and sends them to the backend.  
2. **Backend (FastAPI)**:  
   - Hosts `/predict` API endpoint  
   - Loads pre-trained ML model and TF-IDF vectorizer  
   - Returns prediction (Safe / Unsafe) to frontend  
3. **ML Layer (Scikit-learn)**: Processes vectorized input to generate predictions  

---

## 6. Features

1. Real-time message prediction  
2. Safe / Unsafe classification  
3. Rule-based auto-labeling for common unsafe patterns (URLs, OTPs, urgent keywords)  
4. Synthetic augmentation to enhance model accuracy  
5. Download chat history as `.txt`

---

## 7. Local Setup Instructions

 #7.1 project-folder/
 
├─Chatbot info/
 │   ├─ ml_backend/
       ├─ dataset_cleaned.csv 
      ├─ main.py           # FastAPI backend code
      ├─ app.py # ML training script
      ├─ se_detector_model.pkl
      └─ vectorizer.pkl
│   └─ app/              # Next.js frontend app
       └─ api/
              └─ chat-stream/
                   └─ route.ts/
├─ README.md       
# 7.2 Installation Instructions
Clone the repository:
Gitclone https://github.com/Khadija-tulkubra/AI_Chatbot-for-social-engineering-attack-detection
            cd Chatbot Info
Backend Setup:
           cd ml_backend
           pip install -r requirements.txt  # FastAPI, scikit-learn, pandas, joblib
           uvicorn main:app --reload --port 8000
Frontend Setup:
 npm install
            npm run dev

Open your browser and access frontend at http://localhost:3000.

<img width="1366" height="718" alt="image" src="https://github.com/user-attachments/assets/a02897a4-a1a6-44b1-9a96-0af7ba52209f" />



Chat with the bot and see safe/unsafe predictions.






