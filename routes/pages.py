from flask import Blueprint, render_template, request

from summarygenerator import SUMMARY_LENGTHS, summarize
from .utils import check_text


pages = Blueprint('pages', __name__)


@pages.route('/', methods=['GET', 'POST'])
def home():
    text = ''
    length = 'medium'
    result = None
    error = None

    if request.method == 'POST':
        text = request.form.get('text', '')
        length = request.form.get('length', 'medium')

        if length not in SUMMARY_LENGTHS:
            length = 'medium'

        error = check_text(text)
        if not error:
            result = summarize(text, SUMMARY_LENGTHS[length])

    return render_template(
        'index.html',
        active_page='home',
        text=text,
        length=length,
        result=result,
        error=error,
    )


@pages.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html', active_page='how')
