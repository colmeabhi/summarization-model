import os


class Config:
    # change this with an environment variable when deploying
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-me')

    # debug mode should never be on in production (the debugger lets
    # anyone run code on the server)
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'

    # dont accept huge requests (1 MB)
    MAX_CONTENT_LENGTH = 1024 * 1024

    # max number of characters we try to summarise, bigger texts are slow
    MAX_TEXT_LENGTH = 20000

    PORT = int(os.environ.get('PORT', 5001))
