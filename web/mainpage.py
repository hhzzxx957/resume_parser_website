import sys
sys.path.append('../pyresparser')
from resparser import ResumeParser
# data1 = ResumeParser('resume/Resume_Jason(ZhixingHe).pdf').get_extracted_data()
from flask import Flask, render_template, flash, request, redirect
# from wtforms import Form, TextField, validators
import os

# App config.
DEBUG = True
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'docx', 'pdf'}

# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def mainpage():
    results = {}
    if request.method == 'POST':

        if request.form.get('submit') == 'Submit':
            if not request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files["myfile"]
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            saved_file = '/'.join([UPLOAD_FOLDER, filename])
            results = ResumeParser(saved_file).get_extracted_data()
            # results['test'] = 'test'

    return render_template('index.html', results = results)


if __name__ == "__main__":
    app.run()
