from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, make_response
import ml

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def home():
    prediction = 'hi'
    return render_template('homepage.html', prediction=prediction)

@app.route('/predict', methods=['POST'])
def predict():
    req = request.get_json()
    image = req['image']
    prediction = ml.predict(image)
    res = make_response(jsonify({'JSON': prediction}))
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)