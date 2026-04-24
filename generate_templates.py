import os

os.makedirs("templates", exist_ok=True)

# ── candidates.html ──────────────────────────────────────────
candidates_html = """\
{% extends "base.html" %}
{% block content %}
<div class="page-header">
  <h1>Candidate Management</h1>
  <p>Add and configure candidates with factor scores</p>
</div>
<div class="section-row">
<div class="card">
  <div class="card-title">Add New Candidate</div>
  <form method="POST" action="/candidates">
    <div class="form-row">
      <div class="form-group"><label>Name</label><input name="name" required placeholder="Candidate name"></div>
      <div class="form-group"><label>Party</label><input name="party" required placeholder="Party name"></div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label>Constituency</label>
        <select name="constituency_id">
          {% for c in constituencies %}<option value="{{ c.id }}">{{ c.name }}</option>{% endfor %}
        </select>
      </div>
      <div class="form-group">
        <label>Color</label>
        <input type="color" name="color" value="#7c3aed" style="height:38px;padding:4px">
      </div>
    </div>
    <div class="form-group">
      <label><input type="checkbox" name="is_incumbent"> Is Incumbent?</label>
    </div>
    {% set factor_labels = [
      ("incumbency_score","Incumbency Score"),
      ("party_strength","Party Strength"),
      ("past_work_score","Past Work / OSINT"),
      ("personal_base","Personal Base"),
      ("caste_base","Caste/Religious Base"),
      ("digital_sentiment","Digital Sentiment")
    ] %}
    {% for fname, label in factor_labels %}
    <div class="form-group">
      <label>{{ label }} <span id="{{ fname }}_val" style="color:#a78bfa">50</span>/100</label>
      <input type="range" name="{{ fname }}" min="0" max="100" value="50"
             oninput="document.getElementById('{{ fname }}_val').textContent=this.value">
    </div>
    {% endfor %}
    <button type="submit" class="btn btn-primary">Add Candidate</button>
  </form>
</div>

<div style="flex:1">
  <div class="card">
    <div class="card-title">All Candidates</div>
    {% if candidates %}
    <table>
      <thead>
        <tr><th>Name</th><th>Party</th><th>Incumbent</th><th>Score</th><th></th></tr>
      </thead>
      <tbody>
      {% for c in candidates %}
      <tr>
        <td style="font-weight:500">{{ c.name }}</td>
        <td>{{ c.party }}</td>
        <td>
          {% if c.is_incumbent %}
            <span class="badge badge-high">Yes</span>
          {% else %}
            <span class="badge badge-neu">No</span>
          {% endif %}
        </td>
        <td style="color:{{ c.color }}">
          {{ ((c.incumbency_score*0.15 + c.party_strength*0.20 + c.past_work_score*0.20
               + c.personal_base*0.15 + c.caste_base*0.20 + c.digital_sentiment*0.10))|round(1) }}
        </td>
        <td>
          <a href="/candidate/delete/{{ c.id }}" class="btn btn-danger"
             style="padding:4px 10px;font-size:12px;text-decoration:none"
             onclick="return confirm('Delete this candidate?')">Delete</a>
        </td>
      </tr>
      {% endfor %}
      </tbody>
    </table>
    {% else %}
    <p style="color:var(--muted)">No candidates yet.</p>
    {% endif %}
  </div>

  <div class="card">
    <div class="card-title">Add Constituency</div>
    <form method="POST" action="/constituency/add">
      <div class="form-row">
        <div class="form-group"><label>Name</label><input name="name" required placeholder="Constituency name"></div>
        <div class="form-group"><label>State</label><input name="state" required placeholder="State"></div>
      </div>
      <div class="form-group">
        <label>Total Voters</label>
        <input name="total_voters" type="number" value="100000">
      </div>
      <button type="submit" class="btn btn-primary">Add Constituency</button>
    </form>
  </div>
</div>
</div>
{% endblock %}
"""

# ── forecast.html ─────────────────────────────────────────────
forecast_html = """\
{% extends "base.html" %}
{% block content %}
<div class="page-header">
  <h1>PoW Scenario Forecast</h1>
  <p>Probability of Win across 4 turnout and swing-voter scenarios</p>
</div>

<div style="display:flex;align-items:center;gap:12px;margin-bottom:20px">
  <label style="margin:0;width:auto;font-size:13px">Constituency:</label>
  <select class="constituency-select"
          onchange="location.href='/forecast?constituency_id='+this.value">
    {% for c in constituencies %}
    <option value="{{ c.id }}"
      {% if selected and selected.id == c.id %}selected{% endif %}>{{ c.name }}</option>
    {% endfor %}
  </select>
</div>

{% if scenarios %}
<div class="card">
  <div class="card-title">Scenario Comparison — Probability of Win (%)</div>
  <canvas id="scenarioChart" style="max-height:320px"></canvas>
</div>

<div class="card">
  <div class="card-title">Scenario Breakdown Table</div>
  <table>
    <thead>
      <tr>
        <th>Candidate</th>
        <th>Base (65%)</th>
        <th>High Turnout (80%)</th>
        <th>Low Turnout (50%)</th>
        <th>Anti-Wave (70%)</th>
      </tr>
    </thead>
    <tbody>
    {% for c in candidates %}
    <tr>
      <td style="font-weight:500;color:{{ c.color }}">{{ c.name }}</td>
      <td>{{ scenarios.base.get(c.name, 0) }}%</td>
      <td>{{ scenarios.high_turnout.get(c.name, 0) }}%</td>
      <td>{{ scenarios.low_turnout.get(c.name, 0) }}%</td>
      <td>{{ scenarios.anti_wave.get(c.name, 0) }}%</td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
</div>

<script>
const scenarios = {{ scenarios|tojson }};
const candidateNames = {{ candidates|map(attribute='name')|list|tojson }};
const colors = {{ candidates|map(attribute='color')|list|tojson }};
const labels = ['Base (65%)', 'High Turnout (80%)', 'Low Turnout (50%)', 'Anti-Wave (70%)'];
const scenarioKeys = ['base', 'high_turnout', 'low_turnout', 'anti_wave'];
const datasets = candidateNames.map((name, i) => ({
  label: name,
  data: scenarioKeys.map(k => scenarios[k]?.[name] || 0),
  backgroundColor: colors[i] + 'cc',
  borderColor: colors[i],
  borderWidth: 1,
  borderRadius: 4
}));
new Chart(document.getElementById('scenarioChart'), {
  type: 'bar',
  data: { labels, datasets },
  options: {
    responsive: true,
    plugins: { legend: { labels: { color: '#e8e8f0' } } },
    scales: {
      x: { ticks: { color: '#8888aa' }, grid: { color: 'rgba(255,255,255,0.05)' } },
      y: {
        ticks: { color: '#8888aa', callback: v => v + '%' },
        grid: { color: 'rgba(255,255,255,0.05)' },
        max: 100
      }
    }
  }
});
</script>

{% else %}
<div class="card" style="text-align:center;padding:48px">
  <p style="color:var(--muted)">
    No candidates found. <a href="/candidates" style="color:#a78bfa">Add some</a>
  </p>
</div>
{% endif %}
{% endblock %}
"""

with open("templates/candidates.html", "w", encoding="utf-8") as f:
    f.write(candidates_html)

with open("templates/forecast.html", "w", encoding="utf-8") as f:
    f.write(forecast_html)

print("Templates created successfully!")# 1. Generate templates