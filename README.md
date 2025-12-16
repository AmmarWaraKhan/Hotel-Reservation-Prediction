# 🏨 Hotel Reservation Prediction (MLOps Project)
## 📌 Project Overview
This project predicts whether a hotel customer will honor or cancel a reservation using Machine Learning.
It is designed as a complete end-to-end MLOps pipeline, covering data ingestion, model training, experiment tracking, CI/CD, containerization, and cloud deployment.

The project follows industry-grade MLOps practices using:

1. Python
2. Scikit-learn
3. Docker
4. Jenkins (CI/CD)
5. Google Cloud (GCR + Cloud Run)

## 🎯 Business Problem
1. Revenue management
2. Inventory planning
3. Marketing strategy

### Goal:
Predict reservation cancellations in advance so hotels can take proactive actions.

### 🧠 Use Cases
1. Revenue optimization
2. Targeted marketing campaigns
3. Fraud detection and anomaly identification


## ⚙️ Tech Stack
1. Category	Tools
2. Language	Python 3.11
3. ML	scikit-learn, pandas, numpy
4. Experiment Tracking	MLflow
5. CI/CD	Jenkins
6. Containerization	Docker
7. Cloud	Google Cloud (GCR, Cloud Run)
8. Version Control	Git & GitHub


## 🔁 MLOps Workflow

1. Project Setup
2. Data Ingestion
3. Data Processing
4. Model Training
5. Experiment Tracking (MLflow)
6. Training Pipeline
7. Dockerization
8. CI/CD with Jenkins
9. Push Image to Google Container Registry (GCR)
10. Deploy to Google Cloud Run


## 🧪 Training Pipeline
python pipeline/training_pipeline.py

This pipeline includes:

1. Data loading
2. Feature engineering
3. Model training
4. Model evaluation
5. Artifact saving
⚠️ The training pipeline is intentionally kept and runs during Docker build for reproducibility.



## 🐳 Docker

### Build Docker Image
docker build -t ml-project .

### Run Locally
docker run -p 8080:8080 ml-project

## 🚀 CI/CD with Jenkins

Jenkins pipeline performs:

1. GitHub checkout
2. Docker build
3. Image push to GCR
4. Deployment to Google Cloud Run
5. Triggered automatically on GitHub push.


## 🧾 Dataset
Public hotel reservation dataset

## 👨‍💻 Author

Ammar Wara Khan
MSc Data Science & Applications
Focus: Data Science, MLOps, Cloud Deployment
