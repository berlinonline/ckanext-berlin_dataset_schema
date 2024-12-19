# coding: utf-8
"""Tests for schema.py."""

import logging

import pytest

import ckanext.berlin_dataset_schema.schema as schema
from ckanext.berlin_dataset_schema.tests import empty_schema, berlin_od_schema

log = logging.getLogger(__name__)
PLUGIN_NAME = 'berlin_dataset_schema'

class TestCompleteSchema(object):

    def test_author_property_is_required(self, berlin_od_schema):
        assert schema.Schema().required('author') is True

    def test_maintainer_property_is_not_required(self, berlin_od_schema):
        assert schema.Schema().required('maintainer') is False

    def test_schema_contains_group_property(self, berlin_od_schema):
        assert schema.Schema().contains('groups') is True

    def test_schema_does_not_contain_id_property(self, berlin_od_schema):
        assert schema.Schema().contains('id') is False

    def test_geographical_granularity_property_has_type_string(self, berlin_od_schema):
        assert schema.Schema().attribute_type('geographical_granularity') == 'string'

    def test_groups_property_has_type_array(self, berlin_od_schema):
        assert schema.Schema().attribute_type('groups') == 'array'

    def test_non_existant_property_has_type_none(self, berlin_od_schema):
        assert schema.Schema().attribute_type('foo_bar') is None

    def test_enum_for_attribute_returns_correct_list(self, berlin_od_schema):
        expected_list = [ 'datensatz', 'dokument', 'app' ]
        assert schema.Schema().enum_for_attribute('berlin_type').sort() is expected_list.sort()

    def test_enum_for_attribute_returns_none_for_unenumerated(self, berlin_od_schema):
        assert schema.Schema().enum_for_attribute('author') is None

    def test_attribute_definition_for_existing_attribute_is_dict(self, berlin_od_schema):
        definition = schema.Schema().attribute_definition('geographical_coverage')
        assert isinstance(definition, dict)
    
    def test_attribute_definition_for_missing_attribute_is_none(self, berlin_od_schema):
        assert schema.Schema().attribute_definition('foo') is None
    
    def test_enum_for_attribute_raises_error_for_undefined_attribute(self, berlin_od_schema):
        with pytest.raises(schema.SchemaError):
            schema.Schema().enum_for_attribute('foo_bar')

class TestEmptySchema(object):

    def test_empty_schema_raises_schema_error_on_enum_for_attribute(self, empty_schema):
        with pytest.raises(schema.SchemaError):
            schema.Schema().enum_for_attribute('author')

    def test_empty_schema_raises_schema_error_on_attribute_type(self, empty_schema):
        with pytest.raises(schema.SchemaError):
            schema.Schema().attribute_type('author')

    def test_empty_schema_raises_schema_error_on_contains(self, empty_schema):
        with pytest.raises(schema.SchemaError):
            schema.Schema().contains('author')

    def test_empty_schema_raises_schema_error_on_required(self, empty_schema):
        with pytest.raises(schema.SchemaError):
            schema.Schema().required('author')

    def test_empty_schema_raises_schema_error_on_attribute_definition(self, empty_schema):
        with pytest.raises(schema.SchemaError):
            schema.Schema().attribute_definition('author')

class TestNoSchemaLoaded(object):

    def test_accessing_schema_without_loading_raises_attribute_error(self):
        with pytest.raises(schema.SchemaError):
            schema.Schema().required('author')
    