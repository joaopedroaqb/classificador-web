from app.validacao import classificar_imagem
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_restful import Api
import os

app = Flask(__name__)
app.static_url_path = '/static'

@app.route("/api",methods = ['GET','POST'])
def api():
    imagem = request.files['image']
    resultado = classificar_imagem(imagem)
    return {"message": resultado}

UPLOAD_FOLDER = 'app/static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    dir = os.listdir(app.config['UPLOAD_FOLDER'])
    for i in range(0, len(dir)):
        os.remove(app.config['UPLOAD_FOLDER']+dir[i])
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        imagem = request.files.get('file')
        if not imagem:
            return
        filename = secure_filename("uploads/"+imagem.filename)
        imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resultado = classificar_imagem(imagem)
        return render_template('result.html', result=resultado, filename=filename)
    return render_template('index.html')

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='/uploads/' + filename), code=301)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/infiltracao')
def infiltacao():
    return render_template('infiltracao.html')

@app.route('/efusao')
def efusao():
    return render_template('efusao.html')

@app.route('/atelectasia')
def atelectasia():
    return render_template('atelectasia.html')

@app.route('/nodulo')
def nodulo():
    return render_template('nodulo.html')


if __name__ == '__main__':
    app.run(debug=True)
