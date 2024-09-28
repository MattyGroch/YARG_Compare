from flask import Flask, render_template, request, jsonify
import json
from fuzzywuzzy import fuzz
import os

app = Flask(__name__)

def fuzzy_match(str1, str2, threshold=80):
    return fuzz.ratio(str1.lower(), str2.lower()) >= threshold

def compare_songs(list_a, list_b):
    common = []
    missing_from_a = []
    missing_from_b = []

    for song_b in list_b:
        match_found = False
        for song_a in list_a:
            if (fuzzy_match(song_a['Name'], song_b['Name']) and
                song_a['Artist'] == song_b['Artist'] and
                song_a['Charter'] == song_b['Charter']):
                common.append(song_a)
                match_found = True
                break
        if not match_found:
            missing_from_a.append(song_b)

    for song_a in list_a:
        if not any(fuzzy_match(song_a['Name'], song_b['Name']) and
                   song_a['Artist'] == song_b['Artist'] and
                   song_a['Charter'] == song_b['Charter'] for song_b in list_b):
            missing_from_b.append(song_a)

    return common, missing_from_a, missing_from_b

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    file_a = request.files['file_a']
    file_b = request.files['file_b']
    label_a = request.form['label_a']
    label_b = request.form['label_b']

    list_a = json.load(file_a)
    list_b = json.load(file_b)

    common, missing_from_a, missing_from_b = compare_songs(list_a, list_b)

    return jsonify({
        'common': common,
        'missing_from_a': missing_from_a,
        'missing_from_b': missing_from_b,
        'label_a': label_a,
        'label_b': label_b
    })

if __name__ == '__main__':
    app.run(debug=True)