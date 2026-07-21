from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent
model = joblib.load(BASE_DIR / "loan_prediction_model.pkl")
