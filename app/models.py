from app import db
import json

class Constituency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(80))
    total_voters = db.Column(db.Integer)
    demographics = db.Column(db.Text)  # JSON string

    def get_demographics(self):
        return json.loads(self.demographics or "{}")

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    party = db.Column(db.String(80))
    is_incumbent = db.Column(db.Boolean, default=False)
    constituency_id = db.Column(db.Integer, db.ForeignKey("constituency.id"))

    # Matrix factor scores (0-100)
    incumbency_score = db.Column(db.Float, default=50.0)
    party_strength   = db.Column(db.Float, default=50.0)
    past_work_score  = db.Column(db.Float, default=50.0)
    personal_base    = db.Column(db.Float, default=50.0)
    caste_base       = db.Column(db.Float, default=50.0)
    digital_sentiment= db.Column(db.Float, default=50.0)

    color = db.Column(db.String(20), default="#7c3aed")