# Student AI Workflow

## Overview
This project is part of the **Microsoft Elevate Internship (December 2025 Batch)**.  
It extends a Power BI student marks dashboard into an **AI-powered workflow** using Python, Copilot, and Power Automate.

## Features
- Student marks dataset (Excel) for analysis
- Power BI dashboard with KPIs, grade distribution, and subject averages
- Python ML pipeline (scikit-learn) for pass/fail and grade prediction
- Copilot-generated insights and recommendations
- Power Automate workflow for automation and reporting

## Tech Stack
- Python (pandas, scikit-learn, joblib, openpyxl)
- Power BI Desktop
- Microsoft Power Automate
- Microsoft Copilot

## Project Structure
```
student-ai-workflow/
├─ data/          # raw and processed datasets
├─ models/        # saved ML models
├─ scripts/       # training and pipeline scripts
├─ powerbi/       # Power BI dashboard (.pbix)
└─ requirements.txt
```

## How to Run
1. Create virtual environment:
   ```
   python -m venv venv
   .\venv\Scripts\Activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Train model:
   ```
   python scripts/train_model.py
   ```
4. Run pipeline:
   ```
   python scripts/run_pipeline.py
   ```
5. Open Power BI dashboard and refresh.

---

*This README is a short version. More details, screenshots, and documentation will be added later.*
```

---
