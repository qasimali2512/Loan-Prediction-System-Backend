from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import joblib
from pathlib import Path

from app.schema import LoanInput

app = FastAPI(
    title="Loan Prediction API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



BASE_DIR = Path(__file__).resolve().parent
model = joblib.load(BASE_DIR / "loan_prediction_model.pkl")

FEATURES = [
    "Gender",
    "Married",
    "Dependents",
    "Education",
    "Self_Employed",
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History",
    "Property_Area_Semiurban",
    "Property_Area_Urban"
]


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Loan Prediction API Running"
    }


@app.post("/predict", status_code=status.HTTP_200_OK)
def predict(data: LoanInput):

    try:

        gender = 1 if data.Gender == "Male" else 0

        married = 1 if data.Married == "Yes" else 0

        education = 1 if data.Education == "Graduate" else 0

        self_employed = 1 if data.Self_Employed == "Yes" else 0

        credit = 1 if data.Credit_History == "Good" else 0

        if data.Property_Area == "Urban":

            semiurban = 0
            urban = 1

        elif data.Property_Area == "Semiurban":

            semiurban = 1
            urban = 0

        else:

            semiurban = 0
            urban = 0

        df = pd.DataFrame([{

            "Gender": gender,

            "Married": married,

            "Dependents": data.Dependents,

            "Education": education,

            "Self_Employed": self_employed,

            "ApplicantIncome": data.ApplicantIncome,

            "CoapplicantIncome": data.CoapplicantIncome,

            "LoanAmount": data.LoanAmount,

            "Loan_Amount_Term": data.Loan_Amount_Term,

            "Credit_History": credit,

            "Property_Area_Semiurban": semiurban,

            "Property_Area_Urban": urban

        }])

        df = df[FEATURES]

        prediction = model.predict(df)[0]

        probability = model.predict_proba(df)[0]

        confidence = round(max(probability) * 100, 2)

        result = "Loan Approved" if prediction == 1 else "Loan Rejected"

        return {

            "status": "success",

            "prediction": result,

            "confidence": f"{confidence}%"

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
