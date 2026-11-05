# coding: utf-8
from flask import Flask, jsonify, render_template, request

from summarygenerator import summarize


app = Flask(__name__)


@app.route('/')
def index():
    """Serve a minimal UI for interacting with the summariser."""
    return render_template('index.html')


@app.route('/post_summary', methods=['POST'])
def summary_creator():
    request_data = request.get_json()
    if not request_data or 'textString' not in request_data:
        return jsonify({'error': 'textString is required'}), 400

    text = request_data['textString']
    result = summarize(text)

    return jsonify({'summary': result['summary']})


if __name__ == '__main__':
    app.run(debug=True, port=5001)

