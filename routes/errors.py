from flask import Blueprint, jsonify, render_template, request


errors = Blueprint('errors', __name__)


def show_error(code, message):
    # api calls get json back, normal pages get the html page
    if request.path.startswith('/api') or request.path == '/post_summary':
        return jsonify({'error': message}), code
    return render_template('error.html', code=code, message=message), code


@errors.app_errorhandler(404)
def not_found(e):
    return show_error(404, 'Sorry, this page does not exist.')


@errors.app_errorhandler(405)
def method_not_allowed(e):
    return show_error(405, 'This method is not allowed here.')


@errors.app_errorhandler(413)
def too_large(e):
    return show_error(413, 'The text you sent is too large.')


@errors.app_errorhandler(500)
def server_error(e):
    return show_error(500, 'Something went wrong on our side, please try again.')
