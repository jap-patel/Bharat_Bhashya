from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = 'static/'

app.secret_key ="cairocoders-ednlan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 *1024 * 1024

ALLOWED_EXTENSIONS = {'mp3','wav','mpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    #  display function code here
    # display_image(file)
    return render_template('index.html')

@app.route('/',methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename =='':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        flash('Image successfully uploaded....')
        return render_template("index.html",filename = filename)
    
    else:
        flash("Allowed audio types are - wav, mop3, mpeg . Kindly upload audion in one of this type..")
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static',filename = '/' + filename),code = 301)

if __name__ == '__main__':
    app.run(debug=True,port=8000)