"""
This module is used to render the main page on web application.

Module defines the following:

Functions, that defines main view;

Variable (main_page) that initiating Blueprint.
"""

from flask import render_template, Blueprint

main_page = Blueprint('main_page', __name__)


@main_page.route('/')
def render_main():
    """
    Returns rendered 'index.html' template for url route '/'

    :return: Rendered 'index.html' template
    """
    return render_template('index.html')
