# encoding: utf-8
"""
Module for handling the import and querying of the JSON Schema for
Datenregister packages.
"""

import json
import ckan.plugins as plugins

class Schema(plugins.SingletonPlugin):
    """
    Class representing the dataset JSON Schema.
    """

    def load_schema(self, schema_path):
        """
        Load the schema.
        """
        if not hasattr(self, '_schema'):
            self._schema = {}
            with open(schema_path) as json_data:
                self._schema = json.load(json_data)

    def unload_schema(self):
        """
        Unload the schema.
        """
        del self._schema

    def schema(self):
        """
        Return the loaded JSON schema as a dict.
        """
        try:
            return self._schema
        except AttributeError:
            raise SchemaError("JSON schema not loaded yet")

    def required(self, attribute):
        """
        Helper function to check if a given dataset attribute is required.
        """
        _required = self.schema().get('required')
        if _required:
            return attribute in _required
        raise SchemaError("JSON Schema does not contain 'required' attribute.")

    def contains(self, attribute):
        """
        Helper function to check if a given dataset attribute is contained in the schema.
        """
        properties = self.schema().get('properties')
        if properties:
            return attribute in properties
        raise SchemaError("JSON Schema does not contain 'properties' attribute.")

    def attribute_type(self, attribute):
        """
        Helper function to return the type of a given dataset attribute, or None if
        it is not contained in the schema.
        """
        properties = self.schema().get('properties')
        if properties:
            if attribute in properties:
                return properties[attribute]['type']
            return None
        raise SchemaError("JSON Schema does not contain 'properties' attribute.")

class SchemaError(BaseException):
    """
    Errors when handling the JSON schema.
    """
