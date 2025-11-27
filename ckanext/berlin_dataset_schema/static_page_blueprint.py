# encoding: utf-8
"""
Blueprint for serving static pages.
"""

from flask import Blueprint

import ckan.lib.base as base


def schema():
    """
    Render the dataset schema documentation page.    
    """
    return base.render('/schema/index.html')

static_page_blueprint = Blueprint('static_page_blueprint', __name__)

# add rules for serving the dataset schema documentation page (/schema/index.html) under `/schema` and `/schema/`
# (flask takes care of redirecting `/schema` to `/schema/`)
static_page_blueprint.add_url_rule(u'/schema/', methods=[u'GET'], view_func=schema)