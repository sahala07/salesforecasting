import os
import pickle
from pathlib import Path

import pandas as pd
from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"
FEATURE_FIELDS = [
    {"name": "store", "label": "Store ID", "type": "number", "icon": "fa-store", "placeholder": "Store ID", "min": 1, "step": 1},
    {"name": "promo", "label": "Promotion (0 or 1)", "type": "number", "icon": "fa-percent", "placeholder": "Promotion", "min": 0, "max": 1, "step": 1},
    {"name": "holiday", "label": "Holiday (0 or 1)", "type": "number", "icon": "fa-calendar-day", "placeholder": "Holiday", "min": 0, "max": 1, "step": 1},
    {"name": "Year", "label": "Year", "type": "number", "icon": "fa-calendar", "placeholder": "Year", "min": 2020, "step": 1},
    {"name": "Month", "label": "Month", "type": "number", "icon": "fa-clock", "placeholder": "Month", "min": 1, "max": 12, "step": 1},
    {"name": "Day", "label": "Day", "type": "number", "icon": "fa-calendar-alt", "placeholder": "Day", "min": 1, "max": 31, "step": 1},
]
FEATURE_NAMES = [field["name"] for field in FEATURE_FIELDS]

app = Flask(__name__, template_folder=str(BASE_DIR / "templates"), static_folder=str(BASE_DIR / "static"))
app.secret_key = os.environ.get("SECRET_KEY", "sales-forecasting-secret")


def load_model():
    if not MODEL_PATH.exists():
        import subprocess
        import sys

        subprocess.run([sys.executable, str(BASE_DIR / "train_model.py")], check=True)

    with MODEL_PATH.open("rb") as file:
        model = pickle.load(file)
    return model


def parse_prediction_form(form_data):
    payload = {}
    for field in FEATURE_FIELDS:
        field_name = field["name"]
        raw_value = form_data.get(field_name, "").strip()
        if not raw_value:
            raise ValueError(f"{field['label']} is required.")

        try:
            if field_name in {"promo", "holiday"}:
                value = int(float(raw_value))
                if value not in {0, 1}:
                    raise ValueError
            elif field_name == "store":
                value = int(float(raw_value))
                if value <= 0:
                    raise ValueError
            elif field_name in {"Year", "Month", "Day"}:
                value = int(float(raw_value))
                if field_name == "Month" and not 1 <= value <= 12:
                    raise ValueError
                if field_name == "Day" and not 1 <= value <= 31:
                    raise ValueError
                if field_name == "Year" and value < 2000:
                    raise ValueError
            else:
                value = float(raw_value)
        except ValueError as exc:
            raise ValueError(f"{field['label']} must be a valid value.") from exc

        payload[field_name] = value

    return payload


@app.route("/")
def home():
    return render_template("index.html", page="home")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            payload = parse_prediction_form(request.form)
            model = load_model()
            input_frame = pd.DataFrame([payload], columns=FEATURE_NAMES)
            prediction = float(model.predict(input_frame)[0])
            rounded_prediction = round(prediction, 2)
            summary = (
                f"This projection estimates sales for store {payload['store']} with "
                f"promo={payload['promo']} and holiday={payload['holiday']} on {payload['Year']}-{payload['Month']}-{payload['Day']}."
            )
            return render_template(
                "result.html",
                prediction=rounded_prediction,
                summary=summary,
                page="predict",
            )
        except Exception as exc:
            flash(str(exc), "danger")
            return redirect(url_for("predict"))

    return render_template("predict.html", page="predict", features=FEATURE_FIELDS)


@app.route("/about")
def about():
    return render_template("about.html", page="about")


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html", page="404"), 404


@app.errorhandler(500)
def internal_server_error(_error):
    return render_template("500.html", page="500"), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
