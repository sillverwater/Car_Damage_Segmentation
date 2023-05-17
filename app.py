from flask import Flask
from flask import request
from flask import render_template
import car_damage_segmentation as car

app = Flask(__name__)

# Main page
@app.route('/')
def index():
    return render_template('index.html')

# 본인차가 아닌 경우
@app.route('/upload_1')
def img_input_1():
    return render_template('input_1.html')

@app.route('/damage_show_1', methods=['GET', 'POST'])
def img_output_1():
    if request.method == 'POST':
        before_img = request.files['before_img']
        before_img.save('./static/images/' + str(before_img.filename))
        before_img_path = './images/' + str(before_img.filename)
        print(before_img_path)

        after_img = request.files['after_img']
        after_img.save('./static/images/' + str(after_img.filename))
        after_img_path = './images/' + str(after_img.filename)
        print(after_img_path)

        b_transfer_img_path, b_damage_message = car.main(str(before_img.filename))
        print(b_transfer_img_path)
        print(b_damage_message)

        a_transfer_img_path, a_damage_message = car.main(str(after_img.filename))
        print(a_transfer_img_path)
        print(a_damage_message)


    return render_template('output_1.html',  before_img = b_transfer_img_path, after_img = a_transfer_img_path, message = a_damage_message)


## 본인 차인 경우
@app.route('/upload_2')
def img_input_2():
    return render_template('input_2.html')

@app.route('/damage_show_2', methods=['GET', 'POST'])
def img_output_2():
    if request.method == 'POST':
        user_img = request.files['user_img']
        user_img.save('./static/images/' + str(user_img.filename))
        user_img_path = './images/' + str(user_img.filename)
        print(user_img_path)

        transfer_img_path, damage_message = car.main(str(user_img.filename))
        print(transfer_img_path)
        print(damage_message)

    return render_template('output_2.html', user_img=user_img_path, transfer_img=transfer_img_path, message = damage_message)


@app.route('/repair_shop')
def repair_shop():
    return render_template('repair_shop.html')

@app.route('/guro')
def guro():
    return render_template('guro.html')
@app.route('/sdm')
def sdm():
    return render_template('sdm.html')
@app.route('/jongno')
def jongno():
    return render_template('jongno.html')


if __name__ == '__main__':
    app.run(debug=True)