from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/annotate')
def annotate():
    return "HERE BE COLORS!"

if __name__ == '__main__':
    app.run(debug=True, port=7001)