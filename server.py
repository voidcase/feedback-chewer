from flask import Flask, render_template, jsonify, request
from word_sentimenter import create_dict
from comment import Comment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/annotate')
def annotate():
    comment_text = request.args.get('comment')
    return jsonify(create_dict(Comment(comment_text)))

if __name__ == '__main__':
    app.run(debug=True, port=7000)