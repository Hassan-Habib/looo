import random
from flask import Flask, request, render_template, jsonify
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

import random


def generate(number):
    vari = ''
    replace_index = number.find('x')  # Find the index of the character to be replaced
    if replace_index != -1:
        vari += number[:replace_index]  # Append everything before the character to be replaced
        vari += str(random.randint(0, 9))  # Replace 'x' with a random number
        vari += number[replace_index + 1:]  # Append everything after the replaced character
    else:
        vari += number

    # Find the index of the '#' symbol
    hash_index = vari.find('#')
    if hash_index != -1:
        vari = vari[:hash_index + 1]  # Keep everything before the '#'
        vari += ''.join([str(random.randint(0, 9)) for _ in range(13)])  # Generate 13 random numbers after the '#'

    print(vari)
    return vari


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/handle_click', methods=['POST', 'GET'])
def handle_click():
    input_text = request.form['inputField']
    generated_text = generate(input_text)

    # Generate QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(generated_text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to a BytesIO object
    qr_img_bytes_io = BytesIO()
    qr_img.save(qr_img_bytes_io)  # Remove format='PNG' argument
    qr_img_bytes_io.seek(0)

    # Convert BytesIO object to base64 encoded string
    qr_img_base64 = base64.b64encode(qr_img_bytes_io.getvalue()).decode('utf-8')
    qr_img_base64_encoded = "data:image/png;base64," + qr_img_base64

    return jsonify({'generated_text': generated_text, 'qr_code_image': qr_img_base64_encoded})


if __name__ == '__main__':
    app.run(debug=True)
