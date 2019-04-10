import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

from keras.models import Sequential, load_model
import keras, sys
import numpy as np
from PIL import Image

classes = ["monkey","boar","crow"]
num_classes = len(classes)
image_size = 50


UPLOAS_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAS_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file'not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            model = load_model('./animal_cnn_aug.h5')

            image = Image.open(sys.argv[1])
            image = image.convert('RGB')
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax()


            #return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <html>
    <head>
    <meta charaset="UTF-8">
    <html><head><title>ファイルをアップロードして判定しよう</title></head>
    <body>
    <h1>ファイルをアップロードして判定しよう！</h1>
    <form method = post enctype = multipart/form-data>
    <p><input type=file name=file>
    <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''

from flask impor 