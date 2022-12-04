import cv2

from flask import Flask
from flask import request
from flask import render_template, redirect, url_for
import car_damage_segmentation as car

app = Flask(__name__)

# Main page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def nst_get():
    return render_template('input.html')

@app.route('/damage_show', methods=['GET', 'POST'])
def nst_post():
    if request.method == 'POST':
        # User Image (target image)
        user_img = request.files['user_img']
        user_img.save('./static/images/' + str(user_img.filename))
        user_img_path = './images/' + str(user_img.filename)
        print(user_img_path)

        transfer_img_path = car.main(str(user_img.filename))
        print(transfer_img_path)

    return render_template('output.html', user_img=user_img_path, transfer_img=transfer_img_path)

if __name__ == '__main__':
    app.run(debug=True)