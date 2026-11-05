from flask import current_app


def check_text(text):
    """Returns an error message if the text is not ok, otherwise None."""
    if not isinstance(text, str) or not text.strip():
        return 'Please enter some text to summarise.'

    max_length = current_app.config['MAX_TEXT_LENGTH']
    if len(text) > max_length:
        return f'Text is too long, please keep it under {max_length} characters.'

    return None
