from flask import Flask, render_template, jsonify, request
from word_sentimenter import create_dict
from comment import Comment
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
    return jsonify({
        'lunch room' : 20,
        'chemistry lab' : -6,
        'doggos' : 500
    })

if __name__ == '__main__':
    app.run(debug=True, port=7000)