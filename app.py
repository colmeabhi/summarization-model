from flask import Flask, jsonify, render_template, request

from config import Config
from summarygenerator import summarize


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
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
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
