# coding: utf-8
"""Tests for validation.py."""

from datetime import datetime
from nose.tools import raises
import ckanext.berlin_dataset_schema.validation as validation
import ckan.lib.navl.dictization_functions as df

# workaround for missing translator object from 
# https://github.com/ckan/ckanext-dcat/commit/bd490115da8087a14b9a2ef603328e69535144bb
from paste.registry import Registry
from ckan.lib.cli import MockTranslator
registry = Registry()
registry.prepare()
from pylons import translator
registry.register(translator, MockTranslator())

def test_isodate_notime_empty_is_none():
    assert validation.isodate_notime('') is None

def test_isodate_notime_datetime_object_is_truncated():    
    assert validation.isodate_notime(datetime(1969, 9, 6, 7, 43, 23, 10)) == "1969-09-06"

def test_isodate_notime_datetime_string_is_truncated():
    assert validation.isodate_notime("1969-09-06T07:43:23.10") == "1969-09-06"

def test_isodate_notime_illegal_string_after_date_is_ignored():
    assert validation.isodate_notime("1969-09-06foo bar") == "1969-09-06"

@raises(df.Invalid)
def test_isodate_notime_datetime_illegal_date_string_raises_invalid_error():
    validation.isodate_notime("foor bar")

@raises(ValueError)
def test_isodate_notime_datetime_date_before_1900_raises_value_error():
    validation.isodate_notime(datetime(1869, 9, 6, 7, 43, 23, 10))

# -------------------

@raises(df.Invalid)
def test_is_berlin_type_raises_invalid_error_for_bad_value():
    validation.is_berlin_type('goo star')

def test_is_berlin_type_gives_correct_answer():
    berlin_types = [ 'datensatz', 'dokument', 'app' ]
    for _type in berlin_types:
        assert validation.is_berlin_type(_type) is _type
