# carebloom
# 🌱 CareBloom – AI Plant Disease Detection & Farmer Support Platform

CareBloom is an AI-powered plant disease detection and farmer-support platform developed as a final-year engineering project. The system analyzes plant images using a deep-learning classification model and provides disease information, plant-health indicators, treatment guidance, weather-based risk information, reminders, consultation support, and other agricultural services.

## 🎯 Project Objective

The main objective of CareBloom is to help farmers and plant growers identify plant diseases quickly and receive useful guidance for plant care and disease management.

## 🤖 AI Disease Detection

CareBloom uses **YOLO11n-cls** from Ultralytics for plant disease image classification.

### Model V2

- Model: YOLO11n-cls
- Image size: 160 × 160
- Number of classes: 106
- Training images: 69,539
- Validation images: 14,869
- Test images: 14,985
- Validation Top-1 Accuracy: 92.5%
- Validation Top-5 Accuracy: 98.8%

The model supports diseases across crops such as:

Apple, Banana, Bean, Bell Pepper, Blackgram, Blueberry, Cabbage, Cauliflower, Cherry, Chilli, Citrus, Coffee, Cucumber, Garlic, Grape, Groundnut, Maize, Maple, Peach, Potato, Radish, Raspberry, Rice, Soybean, Squash, Strawberry, Sugarcane, Tomato, Wheat, and Zucchini.

## ⚙️ Backend Technology Stack

- Python 3.11
- FastAPI
- Uvicorn
- Ultralytics YOLO
- PyTorch
- SQLite
- Open-Meteo Weather API
- Argon2 password hashing
- Git & GitHub

## 🚀 Backend Features

CareBloom currently provides:

- User registration and login
- Secure Argon2 password hashing
- AI plant disease prediction
- Low-confidence prediction protection
- Plant health indicator
- Disease treatment recommendations
- Organic remedy suggestions
- Chemical-treatment guidance
- Disease prevention guidance
- Weather information
- Weather-based disease risk
- Emergency disease alerts
- Plant care schedules
- My Plants
- Disease history
- Disease statistics
- Disease calendar
- Watering and fertilizer reminders
- Plant expert consultation requests and replies
- Government scheme information
- Crop calendar
- Market-price module
- Nearby agricultural-service module
- Farmer community
- Multilingual support
- Rule-based multilingual plant chatbot

## 🌐 Supported Languages

CareBloom backend currently supports:

- English
- Tamil
- Hindi
- Telugu
- Malayalam
- Kannada
- Bengali
- Marathi
- Gujarati
- Punjabi

## 📂 Project Structure

```text
CareBloom/
│
├── backend/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── requirements.txt
│
├── database/
│   └── database.py
│
├── frontend/
│
└── README.md
```

## ▶️ Running the Backend

Clone the repository and move into the project directory.

```bash
git clone https://github.com/haripriya2626/carebloom.git
cd carebloom
```

Create a virtual environment:

```bash
python -m venv backend/venv
```

Activate it on Windows PowerShell:

```powershell
.\backend\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Start the FastAPI server:

```bash
python -m uvicorn backend.main:app --reload
```

Open Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## 🔍 Main Prediction API

```text
POST /api/disease/predict
```

The prediction response can include:

- Plant name
- Disease name
- Model confidence
- Plant health indicator
- Weather conditions
- Weather-based disease risk
- Alert level
- Care schedule
- Organic remedy
- Chemical-treatment guidance
- Prevention advice

## 📊 Plant Health Indicator

The plant-health score is a **rule-based indicator** derived from the predicted disease category.

It should not be interpreted as a medically or scientifically measured percentage of disease severity.

Similarly, model confidence represents how confident the AI model is in its classification and does not represent disease severity.

## ⚠️ Current Limitations

- Disease detection depends on image quality and the classes learned by the trained model.
- The health score is a rule-based plant-health indicator, not a direct measurement of disease severity.
- Weather risk indicates environmental conditions that may favor disease and does not confirm disease occurrence.
- Treatment information is advisory and should not replace guidance from qualified agricultural experts.
- Chemical treatments should be selected and applied according to local agricultural recommendations and expert guidance.
- Market-price data currently uses development/sample data rather than live mandi prices.
- Nearby agricultural services currently require integration with a live maps/places provider.
- Voice chatbot support is planned for future development.

## 🔮 Future Enhancements

- Voice-based farmer assistant
- Live agricultural market-price integration
- Live nearby agricultural-service integration
- Improved disease-severity estimation
- More real-world field-image validation
- Offline disease detection
- Additional crops and diseases
- Sensor and IoT integration
- RC-car/field-monitoring integration

## 👩‍💻 Project

**Project Name:** CareBloom  
**Project Type:** Final Year Engineering Project  
**Domain:** Artificial Intelligence, Machine Learning and Agriculture