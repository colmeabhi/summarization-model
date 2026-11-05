from flask import Blueprint, jsonify, request

from summarygenerator import SUMMARY_LENGTHS, summarize
from .utils import check_text


api = Blueprint('api', __name__)


@api.route('/api/summarize', methods=['POST'])
def summarize_api():
    data = request.get_json(silent=True) or {}
    text = data.get('text')
    length = data.get('length', 'medium')

    error = check_text(text)
    if error:
        return jsonify({'error': error}), 400

    if length not in SUMMARY_LENGTHS:
        return jsonify({'error': 'length must be short, medium or long'}), 400

    result = summarize(text, SUMMARY_LENGTHS[length])
    return jsonify(result)


# old endpoint, kept so the old curl examples still work
@api.route('/post_summary', methods=['POST'])
def post_summary():
    data = request.get_json(silent=True) or {}
    text = data.get('textString')

    error = check_text(text)
    if error:
        return jsonify({'error': error}), 400

    result = summarize(text)
    return jsonify({'summary': result['summary']})
