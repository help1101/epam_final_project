"""
This module is used to render the 'about' page on web application.

Module defines the following:

Functions, that defines 'about' view;

Variable (about) that initiating Blueprint.
"""

from flask import render_template, Blueprint

about = Blueprint('about_page', __name__)


@about.route('/about')
def render_about():
    """
    Returns rendered 'about.html' template for url route '/about'

    :return: Rendered 'about.html' template
    """
    return render_template('about.html')
