# encoding: utf-8
"""
Module for handling the import and querying of the JSON Schema for
Datenregister packages.
"""

import json
import logging
import os

from ckan.plugins import SingletonPlugin

log = logging.getLogger(__name__)

class Schema(SingletonPlugin):
    """
    Class representing the dataset JSON Schema.
    """

    def load_schema(self):
        """
        Load the schema from a local filepath.
        """
        if not hasattr(self, 'schema'):
            log.debug("loading schema...")
            path = os.path.abspath(__file__)
            dir_path = os.path.dirname(path)
            schema_path = os.path.join(dir_path, "public", "schema", "berlin_od_schema.json")

            with open(schema_path) as json_data:
                self.schema = json.load(json_data)
        else:
            log.debug("schema already loaded...")

    def required(self, attribute):
        """
        Helper function to check if a given dataset attribute is required.
        """
        _required = self.schema.get('required')
        if _required:
            return attribute in _required
        return False

    def contains(self, attribute):
        """
        Helper function to check if a given dataset attribute is contained in the schema.
        """
        properties = self.schema.get('properties')
        if properties:
            return attribute in properties
        return False

    def attribute_type(self, attribute):
        """
        Helper function to return the type of a given dataset attribute, or None if
        it is not contained in the schema.
        """
        properties = self.schema.get('properties')
        if properties:
            if attribute in properties:
                return properties[attribute]['type']
        return None
