from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x} and jopel and Pierro"

if __name__ == "__main__":
    app.run()