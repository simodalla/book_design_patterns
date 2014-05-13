# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from flask import redirect, render_template, request, Flask
from werkzeug.exceptions import BadRequest, NotFound

from models import Url

app = Flask(__name__, template_folder='views')


@app.route('/')
def index():
    """Renders main page."""
    return render_template('main_page.html')


@app.route('/shorten/')
def shorten():
    """Returns short_url of requested full_url."""
    # Validate user input
    full_url = request.args.get('url')
    if not full_url:
        raise BadRequest()
    # Model returns object with short_url property
    url_model = Url.shorten(full_url)
    short_url = request.host + '/' + url_model.short_url
    return render_template('success.html', short_url=short_url)


@app.route('/<path:path>')
def redirect_to_full(path=''):
    """Gets short url and redirects user to corresponding full url if found"""
    # Model returns object with full_url property
    url_model = Url.get_by_short_url(path)
    print(url_model)
    print(url_model.full_url)
    # Validate model return
    if not url_model:
        raise NotFound()
    if not url_model.full_url.startswith('http'):
        url_model.full_url = 'http://' + url_model.full_url
        print(url_model.full_url)
    return redirect(url_model.full_url)

if __name__ == '__main__':
    app.run(debug=True)
