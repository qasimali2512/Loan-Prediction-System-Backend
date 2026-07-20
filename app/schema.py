from typing import Literal
from pydantic import BaseModel, Field


class LoanInput(BaseModel):

    Gender: Literal["Male", "Female"]

    Married: Literal["Yes", "No"]

    Dependents: int = Field(..., ge=0, le=3)

    Education: Literal["Graduate", "Not Graduate"]

    Self_Employed: Literal["Yes", "No"]

    ApplicantIncome: float = Field(..., ge=0)

    CoapplicantIncome: float = Field(..., ge=0)

    LoanAmount: float = Field(..., gt=0)

    Loan_Amount_Term: float = Field(..., gt=0)

    Credit_History: Literal["Good", "Bad"]

    Property_Area: Literal[
        "Urban",
        "Semiurban",
        "Rural"
    ]