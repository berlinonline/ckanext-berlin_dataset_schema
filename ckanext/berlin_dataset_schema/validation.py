# coding: utf-8

import logging
from datetime import datetime
from ckan.common import _
import ckan.lib.navl.dictization_functions as df


log = logging.getLogger(__name__)

def isodate_notime(value, context):
    if isinstance(value, datetime):
        return value.date.__format__("%Y-%m-%d")
    if value == '':
        return None
    try:
        date = datetime.strptime(value[:10], "%Y-%m-%d")
        date = date.__format__("%Y-%m-%d")
    except (TypeError, ValueError), e:
        raise df.Invalid(_('Date format incorrect. Use ISO8601: YYYY-MM-DD. Only \
        dates after 1900 allowed!'))
    return date

