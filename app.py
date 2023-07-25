from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image, ImageOps
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.template_folder = 'D:/NGIDING/templates'  # Ubah path ini sesuai dengan direktori templates Anda

# (Fungsi-fungsi dan route lainnya tetap sama)

def apply_sepia_effect(image):
    # Implementasi efek sepia
    width, height = image.size
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            image.putpixel((x, y), (tr, tg, tb))
    return image

def apply_red_effect(image):
    # Implementasi efek merah
    return Image.merge("RGB", (image.split()[0], Image.new("L", image.size, 0), Image.new("L", image.size, 0)))

def apply_blue_effect(image):
    # Implementasi efek biru
    return Image.merge("RGB", (Image.new("L", image.size, 0), Image.new("L", image.size, 0), image.split()[2]))

def apply_green_effect(image):
    # Implementasi efek hijau
    return Image.merge("RGB", (Image.new("L", image.size, 0), image.split()[1], Image.new("L", image.size, 0)))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return redirect(url_for('edit', filename=filename))
    return render_template('index.html')

@app.route('/edit')
def edit():
    filename = request.args.get('filename')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(file_path):
        return render_template('edit.html', file_path=file_path)
    return redirect(url_for('index'))

@app.route('/apply_edit', methods=['POST'])
def apply_edit():
    file_path = request.form['file_path']
    image = Image.open(file_path)

    if image is not None:
        # Konversi gambar ke mode warna RGB
        color_option = request.form.get('color_option')
        if color_option == 'grayscale':
            edited_image = image.convert('L')
        elif color_option == 'sepia':
            edited_image = apply_sepia_effect(image)
        elif color_option == 'invert':
            edited_image = ImageOps.invert(image)
        elif color_option == 'red':
            edited_image = apply_red_effect(image)
        elif color_option == 'blue':
            edited_image = apply_blue_effect(image)
        elif color_option == 'green':
            edited_image = apply_green_effect(image)
        else:
            edited_image = image

        edited_file_path = os.path.join(app.root_path, 'edited', os.path.basename(os.path.splitext(file_path)[0] + '_edited.jpg'))

        # Konversi gambar ke mode RGB sebelum disimpan sebagai format JPEG
        edited_image = edited_image.convert('RGB')
        edited_image.save(edited_file_path)

        return redirect(url_for('result', edited_file_path=edited_file_path))

    return redirect(url_for('index'))

    if os.path.isfile(edited_file_path):
        # Perbaikan di sini, ganti "file_path" dengan "edited_file_path"
        return render_template('result.html', edited_file_path=edited_file_path)
    return redirect(url_for('index'))


@app.route('/edited/<filename>')
def edited_file(filename):
    return send_from_directory('edited', filename)

@app.route('/result')
def result():
    edited_file_path = request.args.get('edited_file_path')
    if os.path.isfile(edited_file_path):
        # Perbaikan di sini, ganti "file_path" dengan "edited_file_path"
        return render_template('result.html', edited_file_path=edited_file_path)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
