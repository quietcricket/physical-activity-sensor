from flask import Flask, request
from datetime import datetime
import os

app=Flask(__name__)

@app.route('/',methods=['POST'])
def save_data():
	filename=datetime.now().strftime('%Y-%m-%d.txt')

	with open(filename,'a') as f:
		f.write(request.data)
		f.write('\n')
	return '1'
	
if __name__ == '__main__':
	app.run(port=8888,host='0.0.0.0')