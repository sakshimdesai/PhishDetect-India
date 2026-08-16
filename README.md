# PhishDetect-India

**ML-powered phishing detection for URLs and SMS — built for how India actually gets scammed.**

PhishDetect-India isn't a generic English-only phishing classifier. It's built to catch scam SMS the way they actually arrive in an Indian inbox — mid-code-switched, half in Hindi or Kannada, half in English — alongside a structural URL-phishing detector, wrapped in a full-stack app with explainable, evidence-backed predictions.

##  What makes this different

Most phishing datasets and demos assume clean English text. That assumption breaks immediately in India, where a scam text looks like this:

> `Aapka bank account block hone wala hai. Abhi KYC verify karo.` `Nimma bank account KYC pending ide. Iga verify madi.`

Instead of forcing every message into English, PhishDetect-India treats **five languages as explicit first-class categories**:

| Language | What it means |
|---|---|
| **English** | Standard English scam/legitimate SMS |
| **Hindi** | Devanagari / native Hindi text |
| **Kannada** | Native Kannada text |
| **Hinglish** | Romanized, code-mixed Hindi-English |
| **Konglish** | Romanized, code-mixed Kannada-English |

It's also tuned to India-specific scam patterns that a Western phishing dataset simply doesn't cover: **KYC scams, account-blocking threats, UPI/cashback lures, prize-winner scams, verification urgency, and courier/delivery fraud.**

### The reward-lure discovery

Early on, the model looked strong on paper — but a targeted stress test using reward/cashback-style phishing messages exposed a real blind spot: accuracy on that category alone was just **18.18%**. A vocabulary audit showed the dataset barely contained words like *won*, *winner*, *prize*, *jeeta*, *sigide*, or *redeem*. Rather than patch the symptom, 60 hand-built, verified non-duplicate reward-phishing samples (across all five languages) were added, and the model was rebuilt from a clean, synchronized dataset → vectorizer → model pipeline. This kind of category-level stress testing — not just trusting an aggregate accuracy number — is baked into how the project was developed.

## Architecture

The system runs **two independent detection pipelines** — SMS and URL — because the two inputs need fundamentally different signals. They're unified behind a single API and a single UI.

```text
                         USER
                          │
                          ▼
                  ┌────────────────┐
                  │  React + Vite  │
                  └───────┬────────┘
                          │  POST /predict
                          ▼
                  ┌────────────────┐
                  │  Flask + CORS  │
                  └───────┬────────┘
                          │
             ┌─────────────┴─────────────┐
             ▼                           ▼
       SMS Predictor               URL Predictor
             │                           │
    TF-IDF + 17 handcrafted        URL structural
         features                     features
             │                           │
       Random Forest               Random Forest
       (XGBoost variant                  │
        also trained)                    │
             └─────────────┬─────────────┘
                          ▼
                Prediction + Confidence
                          │
                     SHAP Explanations
                          │
             ┌─────────────┴─────────────┐
             ▼                           ▼
         React UI                  SQLite Log
             │                           │
             └─────────────┬─────────────┘
                          ▼
                   History / Dashboard

## Tech Stack

### Machine Learning
- **Python 3.11**
- **scikit-learn** — Random Forest classifiers (SMS + URL), TF-IDF vectorization
- **XGBoost** — additional trained SMS classifier variant
- **SHAP** — model explainability for URL predictions, mapped into human-readable reasons
- **pandas / numpy** — data processing and feature engineering
- Custom feature engineering modules (no black-box feature stores):
  - `src/features/sms_features.py` — 17 handcrafted SMS signals
  - `src/features/text_preprocessing.py` — shared train/inference text cleaning
  - `src/features/url_features.py` — 19 structural URL signals
  - `src/explainability/` — SHAP explainers + reason humanization

### Backend
- **Flask** — REST API (`app.py`)
- **Flask-CORS** — enables the Vite dev server to talk to the API locally
- **SQLite** — lightweight persistence layer for every prediction (`database/db.py`)

### Frontend
- **React 19** + **Vite** — chosen deliberately over Streamlit so the project looks and feels like a real product, not a notebook demo
- Component-driven architecture: `Analyzer`, `ResultCard`, `ConfidenceGauge`, `ShapReasons`, `PhishingDNA`, `InvestigationPanel`, `ThreatJourney`, `History`, `Navbar`
- Clean API layer (`frontend/src/api/predict.js`) decoupling networking from presentation

### Tooling
- Jupyter notebooks for exploration and final model training
- Git / GitHub for version control, with trained model artifacts intentionally committed so the pipeline is reproducible end-to-end for collaborators


## Feature Engineering

**SMS (17 handcrafted features + TF-IDF):**
`text_length`, `word_count`, `urgency_keyword_count`, `sensitive_keyword_count`, `action_keyword_count`, `reward_lure_keyword_count`, `url_count`, `contains_url`, `shortened_url_count`, `exclamation_count`, `question_count`, `digit_count`, `uppercase_count`, `uppercase_ratio`, `currency_symbol_count`, `phone_number_count`, `has_sender` — fused with **5,945 TF-IDF features** for a **5,962-dimensional** input vector.

**URL (19 structural features):**
`url_length`, `domain_length`, `subdomain_count`, `has_https`, `is_ip`, `special_char_count`, `digit_count`, `letter_count`, `dot_count`, `hyphen_count`, `underscore_count`, `slash_count`, `question_mark_count`, `equals_count`, `ampersand_count`, `at_symbol_count`, `percent_count`, `obfuscation_count`, `path_length`, `query_length` — no reliance on external threat-intel APIs; every signal is derived directly from the URL string.


##  Model Performance (SMS classifier)

| Metric | Score |
|---|---|
| Accuracy | 99.56% |
| Precision | 99.12% |
| Recall | 100% |
| F1-score | 99.56% |
| ROC-AUC | 99.99% |
| False negatives (test set) | 0 |

Evaluated on a balanced, held-out test set (452 samples) drawn from a final dataset of **2,260 SMS** samples across English, Hindi, Kannada, Hinglish, and Konglish. Also validated with a 10/10 manual multilingual smoke test and a dedicated reward-lure stress test that directly drove the dataset augmentation described above.

> These numbers describe the SMS test-set evaluation specifically — they are not a claim about real-world, in-the-wild performance.

## Application Features

- **Unified `/predict` endpoint** — accepts either an SMS or a URL and routes it to the right pipeline
- **Explainability by default** — SHAP-backed reasons for every URL verdict, surfaced as a "Phishing DNA" signal breakdown rather than a raw score dump
- **Investigation panel** — full raw API response and evidence for anyone who wants to go deeper than the headline verdict
- **Detection pipeline visualization** — a six-stage "Threat Journey" (input → preparation → feature extraction → inference → explainability → verdict) so the analysis process itself is visible, not a black box
- **Persistent history** — every prediction is logged to SQLite and viewable via `GET /history`, not just held in browser session state
- **Production-ready frontend** — clean Vite production build, verified end-to-end (React → Flask → model → SHAP → SQLite → React) across both phishing and legitimate cases for both SMS and URL

## Project Structure
PhishDetect-India/
├── data/
│ ├── raw/ # Source Indian-language SMS + URL datasets
│ └── processed/ # Final cleaned, augmented, balanced dataset
├── models/ # Trained Random Forest / XGBoost artifacts + metadata
├── notebooks/ # Dataset exploration + final training workflow
├── src/
│ ├── features/ # SMS + URL feature engineering, text preprocessing
│ ├── prediction/ # Reusable inference modules (predict_sms, predict_url)
│ └── explainability/ # SHAP explainers + human-readable reason mapping
├── database/ # SQLite init + persistence helpers
├── frontend/ # React + Vite application
│ └── src/
│ ├── api/ # Backend communication layer
│ └── components/ # Analyzer, ResultCard, ShapReasons, History, etc.
├── app.py # Flask API entry point
├── tests/
├── requirements.txt
└── .gitignore

##  Getting Started

```bash
# Backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py                   # runs at http://127.0.0.1:5000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev

API example:
POST /predict
{
  "input": "Aapka bank account block hone wala hai. Abhi KYC verify karo.",
  "input_type": "sms"
}

Roadmap
The core ML pipelines (URL + SMS) and the full application layer (Flask + SQLite + React + SHAP) are complete and verified end-to-end. Open next steps include a unified SMS+URL prediction layer for mixed evidence, cloud deployment, and expanding language coverage beyond the current five categories

Notes
This project was built, tested, and pushed to GitHub with a production-verified Vite build and a fully working local Flask + SQLite backend. No public cloud deployment has been performed yet, so no hosted demo URL is included above.

