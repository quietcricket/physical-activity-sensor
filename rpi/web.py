from flask import Flask, request, render_template
import pandas as pd
import os
from collections import OrderedDict

app = Flask(__name__, template_folder='.')


@app.route('/')
def homepage():
    data = OrderedDict()
    for d in reversed(sorted(os.listdir('pas-data'))):
        files = os.listdir(os.path.join('pas-data', d))
        data[d] = sorted(files)
    return render_template('home.html', data=data)


@app.route('/data', methods=['POST'])
def get_data():
    filename = os.path.join('pas-data', request.form.get('day'), request.form.get('minute') + '.txt')
    data = pd.read_csv(filename)
    data.rolling(5)
    return data.to_string()


if __name__ == '__main__':
    app.run(port=8888, host='0.0.0.0', debug=True)
