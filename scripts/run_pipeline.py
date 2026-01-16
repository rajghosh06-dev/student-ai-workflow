import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

RAW = "data/raw/Student_Marks_Result_Analysis_MS-ELEVATE_CO-PILOT_PROJECT_DATASET_RISHIT-GHOSH.xlsx"
SHEET = "Sheet1"
MODEL_PATH = "models/pass_classifier.pkl"
OUT_DIR = "data/processed"

def build_student_view(df):
    subj_avgs = df.pivot_table(index=["StudentID","Name"],
                               columns="Subject",
                               values="Marks",
                               aggfunc="mean").reset_index()
    subj_avgs.columns.name = None
    mark_cols = [c for c in subj_avgs.columns if c not in ["StudentID","Name"]]
    subj_avgs["OverallAvg"] = subj_avgs[mark_cols].mean(axis=1)
    subj_min = df.groupby(["StudentID","Name"])["Marks"].min().reset_index(name="MinSubjectMark")
    student_view = pd.merge(subj_avgs, subj_min, on=["StudentID","Name"], how="left")
    return student_view

def apply_thresholds(student_view):
    student_view["Rule_Pass"] = ((student_view["OverallAvg"] >= 40) & (student_view["MinSubjectMark"] >= 35)).astype(int)
    student_view["Rule_Grade"] = pd.cut(student_view["OverallAvg"],
                                        bins=[-np.inf, 60, 75, np.inf],
                                        labels=["C","B","A"])
    return student_view

def main():
    # Load raw Excel
    df = pd.read_excel(RAW, sheet_name=SHEET)
    student_view = build_student_view(df)
    student_view = student_view.fillna(student_view.mean(numeric_only=True))

    # Load model and predict
    model = joblib.load(MODEL_PATH)
    feature_cols = [c for c in student_view.columns if c not in ["StudentID","Name","Rule_Pass","Rule_Grade"]]
    X = student_view[feature_cols]
    student_view["Predicted_Pass"] = model.predict(X)

    # Predicted grade using thresholds on OverallAvg
    student_view["Predicted_Grade"] = pd.cut(student_view["OverallAvg"],
                                             bins=[-np.inf, 60, 75, np.inf],
                                             labels=["C","B","A"])

    # Add thresholds for comparison
    student_view = apply_thresholds(student_view)

    # Ensure output directory exists
    os.makedirs(OUT_DIR, exist_ok=True)

    # Save timestamped file (history)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path_ts = os.path.join(OUT_DIR, f"student_predictions_{ts}.csv")
    student_view.to_csv(out_path_ts, index=False)

    # Save/overwrite latest file (for Power BI)
    out_path_latest = os.path.join(OUT_DIR, "student_predictions_latest.csv")
    student_view.to_csv(out_path_latest, index=False)

    print(f"Saved: {out_path_ts}")
    print(f"Updated latest file: {out_path_latest}")

if __name__ == "__main__":
    main()
