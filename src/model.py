import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os


def load_data():
    """Load the sales dataset from data/ folder"""
    csv_path = os.path.join("data", "sales.csv")
    df = pd.read_csv(csv_path)
    return df


def train_model():
    """Train a simple regression model on ad_spend -> units_sold"""
    df = load_data()

    X = df[["ad_spend"]]  # feature (ad_spend)
    y = df["units_sold"]  # target (units_sold)

    model = LinearRegression()
    model.fit(X, y)

    # Save trained model to disk
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/sales_model.pkl")

    return model


def load_model():
    """Load the trained model from disk"""
    return joblib.load("models/sales_model.pkl")


if __name__ == "__main__":
    model = train_model()
    print("✅ Model trained and saved as models/sales_model.pkl")

    # Example prediction
    example_spend = [[400]]
    prediction = model.predict(example_spend)
    print(f"Prediction for ad_spend={example_spend[0][0]} → {prediction[0]:.2f} units sold")
