# coding: utf-8
"""Tests for validation.py."""

from datetime import datetime
from nose.tools import raises
import ckan.lib.navl.dictization_functions as df
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckanext.berlin_dataset_schema.validation as validation

# workaround for missing translator object from 
# https://github.com/ckan/ckanext-dcat/commit/bd490115da8087a14b9a2ef603328e69535144bb
from paste.registry import Registry
from ckan.lib.cli import MockTranslator
registry = Registry()
registry.prepare()
from pylons import translator
registry.register(translator, MockTranslator())

class TestIsodateNotime:
    """
    Tests for validation.isodate_notime() validator.
    """

    def test_isodate_notime_empty_is_none(self):
        assert validation.isodate_notime('') is None

    def test_isodate_notime_datetime_object_is_truncated(self):    
        assert validation.isodate_notime(datetime(1969, 9, 6, 7, 43, 23, 10)) == "1969-09-06"

    def test_isodate_notime_datetime_string_is_truncated(self):
        assert validation.isodate_notime("1969-09-06T07:43:23.10") == "1969-09-06"

    def test_isodate_notime_illegal_string_after_date_is_ignored(self):
        assert validation.isodate_notime("1969-09-06foo bar") == "1969-09-06"

    @raises(df.Invalid)
    def test_isodate_notime_datetime_illegal_date_string_raises_invalid_error(self):
        validation.isodate_notime("foor bar")

    @raises(ValueError)
    def test_isodate_notime_datetime_date_before_1900_raises_value_error(self):
        validation.isodate_notime(datetime(1869, 9, 6, 7, 43, 23, 10))

# -------------------

class TestIsBerlinType:
    """
    Tests for validation.is_berlin_type() validator.
    """

    @raises(df.Invalid)
    def test_is_berlin_type_raises_invalid_error_for_bad_value(self):
        validation.is_berlin_type('goo star')

    def test_is_berlin_type_gives_correct_answer(self):
        berlin_types = [ 'datensatz', 'dokument', 'app' ]
        for _type in berlin_types:
            assert validation.is_berlin_type(_type) is _type

# -------------------

class TestIsGroupNameValid:
    """
    Tests for validation.is_group_name_valid() check.
    """

    def setup(self):
        helpers.reset_db()
        self.groups = []
        group_names = [
            u'arbeit',
            u'bildung',
            u'demographie',
            u'erholung',
            u'geo',
            u'verkehr',
            u'verwaltung'
            u'wahl',
            u'wirtschaft',
            u'wohnen',
        ]
        for group_name in group_names:
            self.groups.append(factories.Group(name=group_name))
        self.user = factories.User()
        for group in self.groups:
            helpers.call_action(
                'member_create',
                id=group['id'],
                object=self.user['id'],
                object_type='user',
                capacity='editor'
            )

    def test_empty_is_an_invalid_group_name(self):
        assert validation.is_group_name_valid('empty', { 'user': self.user['name'] }) is False

    def test_group_names_are_valid_group_names(self):
        for group in self.groups:
            assert validation.is_group_name_valid(group['name'], { 'user': self.user['name'] }) is True
