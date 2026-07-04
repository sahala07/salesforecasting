# Sales Forecasting Flask App

A polished, production-ready Flask application for sales forecasting using a trained machine learning model. The experience is designed to feel like a premium SaaS product with responsive layouts, smooth animation, and a clear prediction workflow.

## Features
- Responsive landing page and marketing-style storytelling
- Prediction form with validation and loading feedback
- Result page with a modern forecast summary
- About page covering the algorithm, dataset, and stack
- Dark mode toggle and polished UI details
- Deploy-ready Flask configuration for Render, Railway, or PythonAnywhere

## Project Structure
```text
SalesForecasting/
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── model.pkl
├── sales.csv
├── templates/
├── static/
└── README.md
```

## Screenshots
Placeholder for screenshots:
- Landing page
- Prediction form
- Results view

## Installation
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run Locally
```bash
python app.py
```
Then open http://127.0.0.1:5000

## VS Code Setup
1. Open the project folder in VS Code.
2. Select the virtual environment as the Python interpreter.
3. Run the app from the integrated terminal.

## Deployment
The app is prepared for deployment on Render, Railway, or PythonAnywhere using Flask and Gunicorn.

## Notes
The model file should be kept alongside the app for local usage and deployment.
