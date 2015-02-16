from flask import Flask, request, render_template

app = Flask('pybotweb')

@app.route('/')
def home():
	return render_template('index.jinja2')