# predictor.py — TrustJob KZ v2.0
# from predictor import predict_single_job, predict_batch_jobs, standardize_job_dataframe

import re, json, warnings, joblib
import numpy as np, pandas as pd
from scipy.sparse import hstack, csr_matrix
warnings.filterwarnings("ignore")

_MODEL_TEXT = joblib.load("models/model_text_only.joblib")
_MODEL_HYB  = joblib.load("models/model_hybrid.joblib")
_TFIDF      = joblib.load("models/tfidf_vectorizer.joblib")
_SCALER     = joblib.load("models/numeric_scaler.joblib")
with open("models/model_config.json") as f: _CFG = json.load(f)
_THRESH_TEXT = _CFG["threshold_text"]
_THRESH_HYB  = _CFG["threshold_hybrid"]
_ML_W        = _CFG["ml_weight"]
_RULE_W      = _CFG["rule_weight"]
_HYB_FEATS   = _CFG["hybrid_features"]
with open("models/suspicious_keywords.json", encoding="utf-8") as f: _KWD = json.load(f)
_ALL_KW = _KWD["en"] + _KWD["ru"] + _KWD.get("kz", [])
with open("models/kz_column_map.json", encoding="utf-8") as f: KZ_MAP = json.load(f)

CANONICAL_TEXT   = ["title","company_profile","description","requirements",
                     "benefits","salary_range","location","employment_type","industry"]
CANONICAL_BINARY = ["telecommuting","has_company_logo","has_questions"]
TRANSLATE_FIELDS = _CFG.get("translate_fields",
    ["title","description","requirements","company_profile","benefits"])

def standardize_job_dataframe(df, source="kaggle"):
    df = df.copy()
    if source == "kazakhstan":
        df = df.rename(columns={k:v for k,v in KZ_MAP.items() if k in df.columns})
    df.columns = [c.lower().strip() for c in df.columns]
    for col in CANONICAL_TEXT:
        if col not in df.columns: df[col] = ""
    for col in CANONICAL_BINARY:
        if col not in df.columns: df[col] = 0
    for col in CANONICAL_TEXT:   df[col] = df[col].fillna("").astype(str)
    for col in CANONICAL_BINARY: df[col] = df[col].fillna(0).astype(int)
    all_cols = CANONICAL_TEXT + CANONICAL_BINARY
    if "fraudulent" in df.columns: all_cols += ["fraudulent"]
    return df[all_cols]

def translate_job_text_to_english(text, enabled=True):
    if not enabled or not isinstance(text, str): return text
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="auto", target="en").translate(text) or text
    except Exception:
        return text

def _clean(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def _rule(text):
    tl = text.lower()
    found = list(set(kw for kw in _ALL_KW if kw in tl))
    return {"suspicious_keyword_count": len(found),
            "local_rule_score": round(min(len(found)/5.0,1.0),4),
            "detected_phrases": found}

def _get_proba(model, X):
    if hasattr(model, "predict_proba"): return float(model.predict_proba(X)[0,1])
    from sklearn.preprocessing import minmax_scale
    return float(minmax_scale(model.decision_function(X).reshape(-1,1))[0,0])

def _risk_lv(score):
    if score < 0.30: return "Low"
    elif score < 0.70: return "Medium"
    return "High"

def _num_row(job):
    raw = " ".join(str(job.get(c,"")) for c in
          ["title","company_profile","description","requirements","benefits"])
    cl = _clean(raw); rule = _rule(raw)
    base = {
        "text_length": len(cl), "word_count": len(cl.split()),
        "missing_salary": int(not bool(job.get("salary_range",""))),
        "missing_company_profile": int(not bool(job.get("company_profile",""))),
        "missing_requirements": int(not bool(job.get("requirements",""))),
        "missing_benefits": int(not bool(job.get("benefits",""))),
        "missing_location": int(not bool(job.get("location",""))),
        "total_missing_fields": sum(int(not bool(job.get(c,"")))
            for c in ["salary_range","company_profile","requirements","benefits"]),
        "suspicious_keyword_count": rule["suspicious_keyword_count"],
        "local_rule_score": rule["local_rule_score"],
        "has_company_logo": int(bool(job.get("has_company_logo",0))),
        "has_questions": int(bool(job.get("has_questions",0))),
        "telecommuting": int(bool(job.get("telecommuting",0))),
    }
    return pd.DataFrame([{k: base.get(k,0) for k in _HYB_FEATS}])

def predict_single_job(job_data, translate_to_english=False, use_hybrid=False):
    job = {k: (translate_job_text_to_english(v, translate_to_english)
               if k in TRANSLATE_FIELDS and isinstance(v,str) else v)
           for k,v in job_data.items()}
    combined = _clean(" ".join(str(job.get(c,"")) for c in
        ["title","company_profile","description","requirements","benefits"]))
    raw = " ".join(str(job_data.get(c,"")) for c in
          ["title","description","requirements","company_profile","benefits"])
    rule_res = _rule(raw)
    X_tfidf = _TFIDF.transform([combined])
    if use_hybrid:
        num_df = _num_row(job)
        X_in   = hstack([X_tfidf, csr_matrix(_SCALER.transform(num_df.fillna(0)))])
        model, thresh = _MODEL_HYB, _THRESH_HYB
    else:
        X_in, model, thresh = X_tfidf, _MODEL_TEXT, _THRESH_TEXT
    ml_prob     = _get_proba(model, X_in)
    final_score = float(_ML_W * ml_prob + _RULE_W * rule_res["local_rule_score"])
    return {
        "prediction": "Fake" if ml_prob >= thresh else "Real",
        "ml_fraud_probability": round(ml_prob,4),
        "local_rule_score": rule_res["local_rule_score"],
        "final_risk_score": round(final_score,4),
        "risk_level": _risk_lv(final_score),
        "detected_suspicious_phrases": rule_res["detected_phrases"],
        "explanation": f"ML={ml_prob:.2f} | rules={rule_res['suspicious_keyword_count']}"
    }

def predict_batch_jobs(df_or_path, source="kazakhstan",
                       translate_to_english=False, use_hybrid=False):
    raw = pd.read_csv(df_or_path) if isinstance(df_or_path,str) else df_or_path.copy()
    std = standardize_job_dataframe(raw, source=source)
    results = [predict_single_job(r.to_dict(),
                   translate_to_english=translate_to_english,
                   use_hybrid=use_hybrid) for _,r in std.iterrows()]
    return pd.concat([raw.reset_index(drop=True), pd.DataFrame(results)], axis=1)
