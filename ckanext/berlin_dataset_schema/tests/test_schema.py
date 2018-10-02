# coding: utf-8
"""Tests for schema.py."""

import os

from nose.tools import with_setup
from nose.tools import raises

import ckanext.berlin_dataset_schema.schema as schema

def instantiate_schema():
    schema.Schema()

def instantiate_and_load_schema():
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    schema_path = os.path.join(dir_path, "resources", "berlin_od_schema.json")
    schema.Schema().load_schema(schema_path)

def instantiate_and_load_empty_schema():
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    schema_path = os.path.join(dir_path, "resources", "berlin_od_schema_empty.json")
    schema.Schema().load_schema(schema_path)

def unload_schema():
    schema.Schema().unload_schema()

@with_setup(instantiate_schema)
@raises(schema.SchemaError)
def test_accessing_schema_without_loading_raises_attribute_error():
    schema.Schema().required('author')

@with_setup(instantiate_and_load_schema, unload_schema)
def test_author_property_is_required():
    assert schema.Schema().required('author') is True

@with_setup(instantiate_and_load_schema, unload_schema)
def test_maintainer_property_is_not_required():
    assert schema.Schema().required('maintainer') is False

@with_setup(instantiate_and_load_empty_schema, unload_schema)
@raises(schema.SchemaError)
def test_empty_schema_raises_schema_error_on_required():
    schema.Schema().required('author')

@with_setup(instantiate_and_load_schema, unload_schema)
def test_schema_contains_group_property():
    assert schema.Schema().contains('groups') is True

@with_setup(instantiate_and_load_schema, unload_schema)
def test_schema_does_not_contain_id_property():
    assert schema.Schema().contains('id') is False

@with_setup(instantiate_and_load_empty_schema, unload_schema)
@raises(schema.SchemaError)
def test_empty_schema_raises_schema_error_on_contains():
    schema.Schema().contains('author')

@with_setup(instantiate_and_load_schema, unload_schema)
def test_geographical_granularity_property_has_type_string():
    assert schema.Schema().attribute_type('geographical_granularity') == 'string'

@with_setup(instantiate_and_load_schema, unload_schema)
def test_groups_property_has_type_array():
    assert schema.Schema().attribute_type('groups') == 'array'

@with_setup(instantiate_and_load_schema, unload_schema)
def test_non_existant_property_has_type_none():
    assert schema.Schema().attribute_type('foo_bar') is None

@with_setup(instantiate_and_load_empty_schema, unload_schema)
@raises(schema.SchemaError)
def test_empty_schema_raises_schema_error_on_attribute_type():
    schema.Schema().attribute_type('author')

