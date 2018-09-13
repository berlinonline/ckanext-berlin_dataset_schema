# coding: utf-8

import logging
from datetime import datetime
from ckan.common import _
from pylons import config
import ckan.lib.navl.dictization_functions as df


log = logging.getLogger(__name__)

<<<<<<< HEAD
def isodate_notime(value):
=======
def berlin_types():
    from ckanext.berlin_dataset_schema.plugin import Berlin_Dataset_SchemaPlugin
    log.debug("schema_ref_url: {}".format(Berlin_Dataset_SchemaPlugin().schema_ref_url()))
    return [
        u'datensatz' ,
        u'dokument' ,
        u'app'
    ]

def isodate_notime(value, context):
>>>>>>> add requiredness to schema, move berlin_types to validation
    if isinstance(value, datetime):
        return value.__format__("%Y-%m-%d")
    if value == '':
        return None
    try:
        date = datetime.strptime(value[:10], "%Y-%m-%d")
        date = date.__format__("%Y-%m-%d")
    except (TypeError, ValueError):
        raise df.Invalid(_('Date format incorrect. Use ISO8601: YYYY-MM-DD. Only \
        dates after 1900 allowed!'))
    return date

def is_berlin_type(value):
    _berlin_types = berlin_types()
    if value in _berlin_types:
        return value
    else:
        raise df.Invalid(_('berlin_type must be one of [ {} ].'.format(', '.join(_berlin_types))))
