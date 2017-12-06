from flask import Flask, render_template, jsonify, request
from word_sentimenter import create_dict
from comment import Comment
from score_predictor import get_coeffs
import wordset

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('overview.html')

@app.route('/annotate')
def annotate():
    comment_text = request.args.get('comment')
    return jsonify(create_dict(Comment(comment_text)))

@app.route('/keywords')
def keywords():
    # mockup
    pairs = get_coeffs()
    dicts = [{'word':word.replace('word_',''), 'score':round(score,3)} for score, word in pairs if type(word) == str]
    return jsonify(dicts)

if __name__ == '__main__':
    app.run(debug=True, port=7001)