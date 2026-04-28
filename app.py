from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    resume = data.get('resume', '')
    job = data.get('job', '')

    prompt = f"""Analyze this resume against the job description and return a JSON response with exactly these fields:
- score: number from 0-100
- matching_keywords: list of keywords found in both
- missing_keywords: list of important keywords from job not in resume
- suggestions: list of 3 improvement suggestions
- summary: one sentence summary

Resume:
{resume}

Job Description:
{job}

Return only valid JSON, no other text, no markdown, no backticks."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    result = json.loads(response.choices[0].message.content)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)