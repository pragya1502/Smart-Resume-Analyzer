from flask import Flask, render_template, request
from utils.extract_text import extract_text_from_pdf, extract_text_from_txt
from utils.analyze_resume import analyze_resume

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Resume file
    if 'resume' not in request.files:
        return "No resume uploaded", 400
    resume_file = request.files['resume']
    resume_text = extract_text_from_pdf(resume_file)

    # Job description (optional)
    job_keywords = None
    if 'jobdesc' in request.files and request.files['jobdesc'].filename != '':
        jd_file = request.files['jobdesc']
        if jd_file.filename.endswith('.pdf'):
            jd_text = extract_text_from_pdf(jd_file)
        else:
            jd_text = extract_text_from_txt(jd_file)
        job_keywords = jd_text.split()  # basic splitting; can improve with NLP

    score, missing_keywords = analyze_resume(resume_text, job_keywords)

    return render_template('result.html', score=score, missing_keywords=missing_keywords)

if __name__ == '__main__':
    app.run(debug=True)
