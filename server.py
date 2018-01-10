from flask import Flask, render_template, jsonify, request
from score_predictor import get_coeffs
from transforms import sentence_split_transform
import maxiv_data
from word_sentimenter import find_context, statements_with
import pickle
import util

app = Flask(__name__)
df = maxiv_data.get_split_set()
df = sentence_split_transform(df)
coeffs = []
try:
    coeffs = pickle.load(open(util.COEFF_PICKLE, 'rb'))
    print('coeffs from pickle')
except FileNotFoundError:
    print('extracting coeffs')
    coeffs = get_coeffs(['nouns','adjectives'])
    pickle.dump(coeffs,open(util.COEFF_PICKLE, 'wb'))


@app.route('/')
def index():
    return render_template('overview.html')


@app.route('/keywords')
def keywords():
    # mockup
    pairs = coeffs
    dicts = [{'word':word, 'score':round(score,3)} for score, word in pairs if type(word) == str]
    return jsonify(dicts)

@app.route('/mentions')
def mentions():
    word = request.args.get('word')
    allstmts = {}
    stmts = {}
    try:
        allstmts = pickle.load(open(util.STMTS_PICKLE, 'rb'))
        if word in allstmts:
            stmts = allstmts[word]
        else:
            raise FileNotFoundError
        print('loaded stmts from pickle')
    except FileNotFoundError:
        print('extracting stmts with contexts and stuff...')
        stmts = statements_with(word, df)
        print('found statements')
        for s in stmts:
            s['highlights'] = find_context(s['text'], word)
        print('found contexts')
        allstmts[word] = stmts
        pickle.dump(allstmts, open(util.STMTS_PICKLE, 'wb'))
    return jsonify(stmts)


if __name__ == '__main__':
    app.run(debug=True, port=7001)