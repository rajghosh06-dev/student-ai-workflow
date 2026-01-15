import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import os

RAW = "data/raw/Student Marks - Result Analysis Dataset.xlsx"
SHEET = "Sheet1"
MODEL_PATH = "models/pass_classifier.pkl"

def build_student_view(df):
    # Pivot to student-level features: average per subject, overall average
    subj_avgs = df.pivot_table(index=["StudentID","Name"],
                               columns="Subject",
                               values="Marks",
                               aggfunc="mean").reset_index()
    subj_avgs.columns.name = None

    # Overall average across subjects
    mark_cols = [c for c in subj_avgs.columns if c not in ["StudentID","Name"]]
    subj_avgs["OverallAvg"] = subj_avgs[mark_cols].mean(axis=1)

    # Subject minimum check (requires merging back or computing per student)
    # Build per-student min across subjects
    subj_min = df.groupby(["StudentID","Name"])["Marks"].min().reset_index(name="MinSubjectMark")
    student_view = pd.merge(subj_avgs, subj_min, on=["StudentID","Name"], how="left")

    # Label: Pass if OverallAvg >= 40 and MinSubjectMark >= 35
    student_view["Pass"] = ((student_view["OverallAvg"] >= 40) & (student_view["MinSubjectMark"] >= 35)).astype(int)

    # Grade by thresholds
    student_view["Grade"] = pd.cut(student_view["OverallAvg"],
                                   bins=[-np.inf, 60, 75, np.inf],
                                   labels=["C","B","A"])
    return student_view

def main():
    df = pd.read_excel(RAW, sheet_name=SHEET)
    student_view = build_student_view(df)

    # Features: subject averages + overall average
    feature_cols = [c for c in student_view.columns if c not in ["StudentID","Name","Pass","Grade"]]
    X = student_view[feature_cols].fillna(student_view[feature_cols].mean())
    y = student_view["Pass"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000))
    ])
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    print(classification_report(y_test, y_pred))

    os.makedirs("models", exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    main()
