# encoding: utf-8

from flask import Blueprint

import ckan.lib.base as base


def schema():
    return base.render('/schema/index.html')

static_page_blueprint = Blueprint('static_page_blueprint', __name__)
static_page_blueprint.add_url_rule(u'/schema', methods=[u'GET'], view_func=schema)
static_page_blueprint.add_url_rule(u'/schema/', methods=[u'GET'], view_func=schema)
static_page_blueprint.add_url_rule(u'/schema/index.html', methods=[u'GET'], view_func=schema)