from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app import db
from app.models import Candidate, Constituency
from app.matrix import compute_pow, compute_weighted_score, get_strategic_gaps
from app.forecasting import run_scenarios
from app.osint import analyze_sentiment

main = Blueprint("main", __name__)

@main.route("/")
def dashboard():
    constituencies = Constituency.query.all()
    sel_id = request.args.get("constituency_id", type=int)
    selected = Constituency.query.get(sel_id) if sel_id else (constituencies[0] if constituencies else None)
    candidates = Candidate.query.filter_by(constituency_id=selected.id).all() if selected else []
    pow_data = compute_pow(candidates) if candidates else {}
    gaps     = get_strategic_gaps(candidates) if candidates else {}
    scores   = {c.name: compute_weighted_score(c) for c in candidates}
    return render_template("dashboard.html",
        constituencies=constituencies, selected=selected,
        candidates=candidates, pow_data=pow_data,
        gaps=gaps, scores=scores)

@main.route("/candidates", methods=["GET","POST"])
def candidates():
    constituencies = Constituency.query.all()
    if request.method == "POST":
        f = request.form
        c = Candidate(
            name=f["name"], party=f["party"],
            is_incumbent="is_incumbent" in f,
            constituency_id=int(f["constituency_id"]),
            incumbency_score=float(f.get("incumbency_score", 50)),
            party_strength=float(f.get("party_strength", 50)),
            past_work_score=float(f.get("past_work_score", 50)),
            personal_base=float(f.get("personal_base", 50)),
            caste_base=float(f.get("caste_base", 50)),
            digital_sentiment=float(f.get("digital_sentiment", 50)),
            color=f.get("color", "#7c3aed"),
        )
        db.session.add(c)
        db.session.commit()
        return redirect(url_for("main.candidates"))
    all_candidates = Candidate.query.all()
    return render_template("candidates.html", candidates=all_candidates, constituencies=constituencies)

@main.route("/constituency/add", methods=["POST"])
def add_constituency():
    f = request.form
    con = Constituency(name=f["name"], state=f["state"],
                       total_voters=int(f.get("total_voters", 100000)), demographics="{}")
    db.session.add(con)
    db.session.commit()
    return redirect(url_for("main.dashboard"))

@main.route("/forecast")
def forecast():
    constituencies = Constituency.query.all()
    sel_id = request.args.get("constituency_id", type=int)
    selected = Constituency.query.get(sel_id) if sel_id else (constituencies[0] if constituencies else None)
    candidates = Candidate.query.filter_by(constituency_id=selected.id).all() if selected else []
    scenarios  = run_scenarios(candidates) if candidates else {}
    return render_template("forecast.html",
        constituencies=constituencies, selected=selected,
        candidates=candidates, scenarios=scenarios)

@main.route("/osint/analyze", methods=["POST"])
def osint_analyze():
    text = request.json.get("text", "")
    return jsonify(analyze_sentiment(text))

@main.route("/candidate/delete/<int:cid>")
def delete_candidate(cid):
    c = Candidate.query.get_or_404(cid)
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for("main.candidates"))