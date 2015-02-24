from pybot import app

@app.route('/')
def home():
	return render_template('index.jinja2')