# handlers.py is the name by convention in flask.

from flask import Blueprint, render_template

error_pages = Blueprint('error_pages', __name__)

@error_pages.app_errorhandler(404)
def error_404(error):
    # return syntax is kinda special to app_errorhandler
    # returns a tuple of the template and the error code
    return render_template('error_pages/404.html'), 404

@error_pages.app_errorhandler(403)
def error_403(error):
    # return syntax is kinda special to app_errorhandler
    # returns a tuple of the template and the error code
    return render_template('error_pages/403.html'), 403
