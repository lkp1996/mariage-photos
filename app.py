import os
import time

from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'heic', 'heif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 Mo max par envoi

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def gallery():
    files = sorted(
        os.listdir(app.config['UPLOAD_FOLDER']),
        key=lambda f: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], f)),
        reverse=True
    )
    files = [f for f in files if allowed_file(f)]
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('photo')
    for file in files:
        if file and allowed_file(file.filename):
            timestamp = str(int(time.time() * 1000))
            filename = secure_filename(f"{timestamp}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            if filename.lower().endswith(('.heic', '.heif')):
                # Conversion en JPEG pour compatibilité universelle
                # (les HEIC d'iPhone ne s'affichent pas nativement dans <img> sur la plupart des navigateurs)
                img = Image.open(file)
                filename = filename.rsplit('.', 1)[0] + '.jpg'
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                img.convert('RGB').save(filepath, 'JPEG', quality=85)
            else:
                file.save(filepath)
    return redirect(url_for('gallery'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/download-all/<secret>')
def download_all(secret):
    import zipfile
    import io
    from flask import send_file

    # Change ce mot de passe avant de déployer !
    if secret != "12092026":
        return "Non autorisé", 403

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename == '.gitkeep':
                continue
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            zf.write(filepath, filename)
    memory_file.seek(0)

    return send_file(memory_file, download_name='photos-mariage.zip', as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
