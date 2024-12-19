import os

import pytest

import ckanext.berlin_dataset_schema.schema as schema

@pytest.fixture
def empty_schema():
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    schema_path = os.path.join(dir_path, "resources", "berlin_od_schema_empty.json")
    schema.Schema().load_schema(schema_path)
    yield
    schema.Schema().unload_schema()

@pytest.fixture
def berlin_od_schema():
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    schema_path = os.path.join(dir_path, "resources", "berlin_od_schema.json")
    schema.Schema().load_schema(schema_path)
    yield
    schema.Schema().unload_schema()

