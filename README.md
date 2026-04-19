# ElectoMatrix – Predictive Electoral Analytics Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge\&logo=flask\&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3.1.1-D71F00?style=for-the-badge\&logo=sqlalchemy\&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?style=for-the-badge\&logo=chartdotjs\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

### Predictive Electoral Analytics Platform

A data-driven political strategy tool that combines demographic data, OSINT, and historical voting patterns into a unified Probability of Win (PoW) engine.

</div>

---

## Overview

ElectoMatrix is a Flask-based electoral analytics platform built for modern political analysis. It allows users to compare multiple candidates across weighted factors such as party strength, incumbency, caste base, sentiment, and historical performance.

The platform is designed to support:

* Candidate comparison
* Constituency-level forecasting
* Sentiment analysis from news and text
* Scenario-based simulations
* Interactive dashboard visualizations

---

## Features

### Candidate Comparison Matrix

* Compare 2 to 4 candidates side by side
* Weighted scoring system across major electoral factors
* Automatic ranking based on total score

### Probability of Win Forecasting

* Softmax-based probability engine
* Base, high-turnout, low-turnout, and anti-wave scenarios
* Dynamic recalculation of candidate win probability

### Sentiment and OSINT Analysis

* TextBlob-powered sentiment analysis
* Optional NewsAPI integration
* Score political narratives and media sentiment

### Dashboard and Visualization

* Chart.js visualizations
* Dark-themed interface
* Interactive scenario comparison charts
* Candidate and constituency management screens

---

## Tech Stack

```text
Backend     → Python 3.10+, Flask, SQLAlchemy, NumPy, TextBlob
Frontend    → HTML, CSS, JavaScript, Chart.js, Plotly
Database    → SQLite
Optional    → NewsAPI for live sentiment feeds
Deployment  → Railway, Render, Gunicorn
```

---

## Project Structure

```text
electoral-analytics/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── matrix.py
│   ├── forecasting.py
│   └── osint.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── candidates.html
│   └── forecast.html
│
├── static/
│   └── style.css
│
├── config.py
├── run.py
├── requirements.txt
└── .gitignore
```

---

## Installation

### Prerequisites

* Python 3.10 or higher
* pip
* Git

### Clone the Repository

```bash
git clone https://github.com/parthsh77/electoral-analytics.git
cd electoral-analytics
```

### Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

If pip is not recognized on Windows:

```bash
py -m pip install -r requirements.txt
```

### Download TextBlob Corpora

```bash
python -m textblob.download_corpora
```

### Run the Application

```bash
python run.py
```

Or:

```bash
py run.py
```

Open your browser at:

```text
http://localhost:5000
```

---

## How It Works

The platform uses a weighted scoring matrix to calculate each candidate’s overall political strength.

Example scoring weights:

```python
WEIGHTS = {
    "incumbency_score": 0.15,
    "party_strength": 0.20,
    "past_work_score": 0.20,
    "personal_base": 0.15,
    "caste_base": 0.20,
    "digital_sentiment": 0.10,
}
```

Each candidate’s score is then passed into a softmax function to calculate the Probability of Win.

---

## Matrix Factors

| Factor                 | Weight | Description                                |
| ---------------------- | ------ | ------------------------------------------ |
| Incumbency Effect      | 15%    | Anti-incumbency or goodwill advantage      |
| Party Strength         | 20%    | Strength of party presence                 |
| Past Work              | 20%    | Development work and political performance |
| Personal Base          | 15%    | Candidate loyalty and local support        |
| Caste / Religious Base | 20%    | Community and identity support             |
| Digital Sentiment      | 10%    | News and social media perception           |

---

## Scenario Forecasting

| Scenario     | Description                              |
| ------------ | ---------------------------------------- |
| Base         | Standard election conditions             |
| High Turnout | Increased voter participation            |
| Low Turnout  | Reduced turnout due to apathy or weather |
| Anti-Wave    | Strong anti-incumbency environment       |

---

## OSINT Integration

The `osint.py` module can analyze sentiment from text.

Example:

```python
from app.osint import analyze_sentiment

result = analyze_sentiment("Candidate has launched major infrastructure projects")
```

Optional NewsAPI integration can be enabled using:

```env
NEWS_API_KEY=your-api-key
```

---

## Configuration

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key
NEWS_API_KEY=your-news-api-key
```

Example configuration:

```python
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///electoral.db"
    DEBUG = True
```

---

## Future Enhancements

* Choropleth map for constituency boundaries
* CSV and Excel import for bulk candidate data
* PDF export of reports
* Multi-user login system
* Historical election data import
* REST API for third-party integrations

---

## Contributing

```bash
git clone https://github.com/parthsh77/electoral-analytics.git
git checkout -b feature/your-feature-name
git add .
git commit -m "feat: describe your change"
git push origin feature/your-feature-name
```

---

## License

This project is licensed under the MIT License.

---

<div align="center">

Built with Python, Flask, SQLAlchemy, and Chart.js.

For educational and research purposes only.

</div>
