#Import Libraries
from flask import Flask, request, render_template, jsonify
import numpy as np
import lstm as model

app = Flask(__name__)

# render htmp page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="4040")