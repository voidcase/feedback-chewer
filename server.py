from flask import Flask, render_template, jsonify, request
from old_word_sentimenter import create_dict
from comment import Comment
from score_predictor import get_coeffs
from new_hope import statements_with
from transforms import sentence_split_transform
import maxiv_data
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

@app.route('/mentions')
def mentions():
    df = maxiv_data.get_split_set()
    df = sentence_split_transform(df)
    print(df['text'])
    return jsonify(statements_with(request.args.get('word'), df))


if __name__ == '__main__':
    app.run(debug=True, port=7001)