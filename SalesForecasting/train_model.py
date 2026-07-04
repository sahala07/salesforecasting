import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "sales.csv"
MODEL_PATH = BASE_DIR / "model.pkl"


def train_and_save_model():
    df = pd.read_csv(DATASET_PATH)
    df = df.dropna()
    df["date"] = pd.to_datetime(df["date"], format="mixed", errors="coerce")
    df = df.dropna(subset=["date"])
    df["Year"] = df["date"].dt.year
    df["Month"] = df["date"].dt.month
    df["Day"] = df["date"].dt.day
    df = df.drop(columns=["date"])

    features = ["store", "promo", "holiday", "Year", "Month", "Day"]
    X = df[features]
    y = df["sales"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions, squared=False)

    print(f"R2 Score: {r2:.3f}")
    print(f"MAE: {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")

    with MODEL_PATH.open("wb") as file:
        pickle.dump(model, file)

    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save_model()
