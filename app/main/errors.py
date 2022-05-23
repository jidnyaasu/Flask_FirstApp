from flask import render_template
from . import main


@main.app_errorhandler(404)
def not_found(e):
    return render_template('error.html', error=e), 404
