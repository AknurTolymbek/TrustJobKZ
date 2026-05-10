# ML Backend Handoff - TrustJobKZ

This folder contains the machine learning part of TrustJobKZ.

## Main ML files

### Models

- `ml/models/model_hybrid.joblib`  
  Main trained model. Uses text and numeric features.

- `ml/models/model_text_only.joblib`  
  Alternative text-only model.

### Artifacts

- `ml/artifacts/tfidf_vectorizer.joblib`  
  Vectorizer for text features.

- `ml/artifacts/numeric_scaler.joblib`  
  Scaler for numeric features.

- `ml/artifacts/model_config.json`  
  Model configuration.

- `ml/artifacts/kz_column_map.json`  
  Column mapping for Kazakhstan job dataset.

- `ml/artifacts/suspicious_keywords.json`  
  Suspicious keywords used for fraud detection.

### Source code

- `ml/src/predictor.py`  
  Python file for loading the model and making predictions.

### Results

- `ml/results/cv_results.csv`
- `ml/results/final_test_metrics.csv`
- `ml/results/model_comparison.csv`

These files show model evaluation results.

## Backend integration idea

Backend developer should load the model and artifacts from the `ml/` folder and use `predictor.py` for fake job detection.

Recommended model for backend:

`ml/models/model_hybrid.joblib`

## Notes

Do not use `__pycache__/` folder. It is only a Python cache folder.