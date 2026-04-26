# AI Based Autism Prediction System

> An end-to-end machine learning web application for early autism spectrum disorder (ASD) screening, built with Python and deployed on Streamlit Cloud.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=flat-square&logo=scikitlearn)

## Live Demo
**[autismdetect.streamlit.app](https://autismdetect.streamlit.app/)**

## About
AI Based Autism Prediction System is an AI-powered screening tool that estimates the likelihood of Autism Spectrum Disorder (ASD) based on demographic information and 10 evidence-based behavioural indicators.

## Features
- 3-step guided screening flow — Personal Info → Behavioural Questions → Result
- Risk level classification — Low / Moderate / High
- Model confidence score with visual percentage bar
- Behavioural score tracker — auto-calculated from 10 questions
- Clean, professional UI with progress indicators

## Model Details
| Property | Details |
|---|---|
| Dataset | UCI Autism Screening Adult Dataset |
| Features | 10 AQ behavioural scores + 8 demographic features |
| Output | Binary classification + probability score |
| Accuracy | ~95% on test set |

## Run Locally
```bash
git clone https://github.com/Mahekjamadar20/NeuroSense.git
cd NeuroSense
pip install -r requirements.txt
streamlit run app.py
```

## Disclaimer
This is an AI screening tool for educational purposes only. Not a substitute for professional medical diagnosis.

## <img width="1296" height="865" alt="1" src="https://github.com/user-attachments/assets/88003fc5-0dc2-42f0-8e3f-96c900b7797b" />
 Author
**Mahek Jamadar** — [@Mahekjamadar20](https://github.com/Mahekjamadar20)
