from textblob import TextBlob
import requests, os

def analyze_sentiment(text: str) -> dict:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity        # -1 to 1
    score = round((polarity + 1) * 50, 1)     # normalize to 0-100
    if polarity > 0.2:
        label = "Positive"
    elif polarity < -0.2:
        label = "Negative"
    else:
        label = "Neutral"
    return {"score": score, "label": label, "polarity": round(polarity, 3)}

def fetch_news_sentiment(query: str) -> dict:
    """Use NewsAPI — get free key at newsapi.org."""
    api_key = os.getenv("NEWS_API_KEY", "")
    if not api_key:
        return {"score": 50.0, "label": "No API key", "polarity": 0}
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize=5&apiKey={api_key}"
    try:
        resp = requests.get(url, timeout=5)
        articles = resp.json().get("articles", [])
        texts = " ".join(a.get("title", "") + " " + a.get("description", "") for a in articles)
        return analyze_sentiment(texts) if texts else {"score": 50.0, "label": "No data", "polarity": 0}
    except Exception:
        return {"score": 50.0, "label": "Error", "polarity": 0}