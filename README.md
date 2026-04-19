<div align="center">
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge&logo=flask&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLAlchemy-3.1.1-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white"/>
<img src="https://img.shields.io/badge/Chart.js-4.4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
<br/><br/>
⚡ ElectoMatrix
Predictive Electoral Analytics Platform
> **A data-driven political strategy tool** that synthesizes OSINT, demographic data, and historical voting patterns into a unified Probability of Win (PoW) engine — built for modern election analysis in complex, multi-candidate constituencies.
<br/>
---
</div>
📌 Table of Contents
Overview
Key Features
Tech Stack
Project Structure
Getting Started
How It Works
The Matrix Model
Scenario Forecasting
OSINT Integration
Configuration
Roadmap
Contributing
License
---
🧭 Overview
Modern elections — especially in demographically complex regions like India — are influenced by an intricate web of overlapping factors: caste dynamics, religious affiliation, incumbency perception, digital sentiment, and historical performance. Yet most political strategists still rely on anecdotal evidence, traditional polling, or local "intuition."
ElectoMatrix changes that.
It provides a multi-dimensional scoring matrix that quantifies these variables side-by-side across all candidates in a constituency, and outputs a clear Probability of Win (PoW) score — updated dynamically as you adjust inputs or run different turnout scenarios.
---
✨ Key Features
Feature	Description
📊 Candidate Comparison Matrix	Stack 2–4 candidates against identical weighted factors in one view
🔮 PoW Forecasting	Softmax-based probability engine with 4 scenario simulations
🧠 OSINT Sentiment Analysis	TextBlob-powered sentiment scoring from news headlines and text input
🗺️ Demographic Mapping	Constituency-level caste and religious base quantification
📉 Strategic Gap Detection	Auto-identifies where each candidate is weakest relative to rivals
🌗 Dark-themed Dashboard	Clean, modern UI with live Chart.js visualizations
🗄️ SQLite Database	Lightweight, zero-config persistent storage via SQLAlchemy
⚙️ Scenario Builder	Base / High Turnout / Low Turnout / Anti-Wave simulations
---
🛠 Tech Stack
```
Backend     →  Python 3.10+, Flask 3.0, SQLAlchemy, NumPy, TextBlob
Frontend    →  Vanilla HTML/CSS, Chart.js 4.4, Plotly
Database    →  SQLite (via Flask-SQLAlchemy)
NLP/OSINT   →  TextBlob, NewsAPI (optional)
Deployment  →  Gunicorn-ready, Railway / Render compatible
```
---
📁 Project Structure
```
electoral-analytics/
│
├── app/
│   ├── __init__.py          # App factory, DB init
│   ├── models.py            # Candidate & Constituency ORM models
│   ├── routes.py            # All Flask route handlers
│   ├── matrix.py            # Core weighted scoring engine
│   ├── forecasting.py       # Scenario-based PoW calculator
│   └── osint.py             # Sentiment analysis module
│
├── templates/
│   ├── base.html            # Sidebar layout shell
│   ├── dashboard.html       # Main comparison matrix view
│   ├── candidates.html      # Candidate add/manage UI
│   └── forecast.html        # Scenario chart & breakdown table
│
├── static/
│   └── style.css            # Dark theme design system
│
├── config.py                # App configuration & secrets
├── run.py                   # Entry point
├── requirements.txt         # Python dependencies
└── .gitignore
```
---
🚀 Getting Started
Prerequisites
Python 3.10 or higher
pip
Git
Installation
```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/electoral-analytics.git
cd electoral-analytics

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLP corpus
python -m textblob.download_corpora

# 5. Run the app
python run.py
```
Open your browser at http://localhost:5000
First Steps in the App
```
1. Go to Candidates → Add a Constituency (e.g. "Lucknow North", "Uttar Pradesh")
2. Add 3 candidates — use sliders to set factor scores (0–100)
3. Return to Dashboard → see the live comparison matrix
4. Visit PoW Forecast → run all 4 scenarios
```
---
⚙️ How It Works
Weighted Scoring Engine (`app/matrix.py`)
Each candidate is scored across 6 matrix factors, each assigned a weight based on constituency-level historical behavior:
```python
WEIGHTS = {
    "incumbency_score":  0.15,   # Positive or anti-incumbency effect
    "party_strength":    0.20,   # National vs regional vs local party power
    "past_work_score":   0.20,   # Verified dev projects, legislative record
    "personal_base":     0.15,   # Previous victory margins, local influence
    "caste_base":        0.20,   # Religious/community block strength
    "digital_sentiment": 0.10,   # OSINT: social media & news perception
}
```
The Probability of Win is calculated via a temperature-scaled softmax:
```python
def compute_pow(candidates):
    scores = np.array([compute_weighted_score(c) for c in candidates])
    exp_scores = np.exp(scores / 20)        # temperature = 20
    pow_values = exp_scores / exp_scores.sum()
    return {c.name: round(float(p) * 100, 1) for c, p in zip(candidates, pow_values)}
```
This ensures PoW values always sum to 100% and spread realistically based on score differences.
---
📐 The Matrix Model
Matrix Factor	Weight	What It Captures
Incumbency Effect	15%	Positive goodwill vs anti-incumbency wave
Party Strength	20%	National presence, regional dominance, or local-only reach
Past Work (OSINT)	20%	Verified development projects, fund utilization, activism record
Personal Base	15%	Traditional loyalists, youth appeal, hyper-local community ties
Caste / Religious Base	20%	Solidified voting blocks vs split or niche identity support
Digital Sentiment	10%	Real-time news & social media perception score
> Weights can be customized per constituency in `app/matrix.py` to reflect local voting dynamics.
---
🔮 Scenario Forecasting
Four scenarios simulate how PoW shifts under different election conditions:
Scenario	Turnout	Swing Factor	Models
Base	65%	1.0×	Standard election day conditions
High Turnout	80%	1.1×	Urban mobilization, strong party machinery
Low Turnout	50%	0.9×	Voter apathy, weather/logistical issues
Anti-Wave	70%	1.3×	Strong anti-incumbency sentiment across the board
Each scenario dynamically adjusts candidate scores and re-runs the PoW engine, displayed as a grouped bar chart.
---
📡 OSINT Integration
The `app/osint.py` module provides two modes of sentiment analysis:
1. Manual Text Analysis
Paste any news article, speech, or social media content:
```python
from app.osint import analyze_sentiment
result = analyze_sentiment("Candidate has launched 12 infrastructure projects...")
# → {"score": 72.4, "label": "Positive", "polarity": 0.448}
```
2. Live NewsAPI Feed (optional — free tier available)
Add your key to a `.env` file:
```
NEWS_API_KEY=your_key_here
```
Get a free key at newsapi.org — 100 requests/day on the free plan.
---
🔧 Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
NEWS_API_KEY=your-newsapi-key-here   # optional
```
All config values are loaded in `config.py`:
```python
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///electoral.db"
    DEBUG = True
```
---
🗺️ Roadmap
[x] Multi-candidate comparison matrix
[x] PoW softmax engine
[x] Scenario forecasting (4 modes)
[x] OSINT sentiment analysis
[x] Dark-themed dashboard
[ ] Choropleth map with India constituency boundaries
[ ] CSV/Excel import for bulk candidate data
[ ] PDF export of full matrix report
[ ] User authentication (multi-strategist access)
[ ] Twitter/X real-time sentiment feed
[ ] Historical election result import (ECI data)
[ ] REST API endpoints for third-party integration
---
🤝 Contributing
Contributions are welcome! Here's how to get started:
```bash
# Fork the repo, then:
git clone https://github.com/YOUR_USERNAME/electoral-analytics.git
git checkout -b feature/your-feature-name

# Make your changes, then:
git add .
git commit -m "feat: describe your change"
git push origin feature/your-feature-name

# Open a Pull Request on GitHub
```
Please keep commits descriptive and focused on a single change.
---
📄 License
This project is licensed under the MIT License — free to use, modify, and distribute with attribution.
---
<div align="center">
Built with Python · Flask · Chart.js
For educational and research purposes. Not affiliated with any political party or electoral body.
</div>