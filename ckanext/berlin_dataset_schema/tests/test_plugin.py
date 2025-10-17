# coding: utf-8
"""Tests for plugin.py."""

import logging
import mock
import pytest

import ckan.logic as logic
import ckan.plugins
from ckan.plugins.toolkit import url_for
import ckan.lib.plugins as lib_plugins
import ckan.lib.navl.dictization_functions as df
import ckan.plugins.toolkit as toolkit
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.model as model

PLUGIN_NAME = 'berlin_dataset_schema'

log = logging.getLogger(__name__)
get_action = logic.get_action

@pytest.mark.ckan_config('ckan.plugins', f"{PLUGIN_NAME}")
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestSchemaGeneration(object):

    @classmethod
    def setup_class(cls):

        cls.required_atomics = [
            "author" ,
            "berlin_source" ,
            "berlin_type" ,
            "date_released" ,
            "license_id" ,
            "maintainer_email" ,
            "name" ,
            "notes" ,
            "title" ,
        ]
        cls.nonrequired_atomics = [
            "attribution_text" ,
            "author_email" ,
            "date_updated" ,
            "geographical_coverage" ,
            "geographical_granularity" ,
            "maintainer" ,
            "temporal_coverage_from" ,
            "temporal_coverage_to" ,
            "temporal_granularity" ,
            "url" ,
            "username" ,
        ]
        cls.required_complex = [
            "groups" ,
        ]
        cls.nonrequired_complex = [
            "resources" ,
            "tags" ,
        ]

    def _test_schema_sanity(self, schema):
        """
        Helper function to test schema feasibility:

        - It's a dict.
        - The values for all known required atomic properties are lists.
        """
        assert isinstance(schema, dict)
        all_atomics = TestSchemaGeneration.required_atomics + \
            TestSchemaGeneration.nonrequired_atomics
        for prop in all_atomics:
            assert isinstance(schema[prop], list)
        all_complex = TestSchemaGeneration.required_complex + \
            TestSchemaGeneration.nonrequired_complex
        for prop in all_complex:
            assert isinstance(schema[prop], dict)

    def test_create_package_schema_looks_sane(self):
        """
        Does the create package schema look feasible?
        """
        package_plugin = lib_plugins.lookup_package_plugin()
        schema = package_plugin.create_package_schema()
        self._test_schema_sanity(schema)

    def test_update_package_schema_looks_sane(self):
        """
        Does the update package schema look feasible?
        """
        package_plugin = lib_plugins.lookup_package_plugin()
        schema = package_plugin.update_package_schema()
        self._test_schema_sanity(schema)

    def test_show_package_schema_looks_sane(self):
        """
        Does the show package schema look feasible?
        """
        package_plugin = lib_plugins.lookup_package_plugin()
        schema = package_plugin.show_package_schema()
        self._test_schema_sanity(schema)

    def test_required_properties_have_not_empty(self):
        """
        The first validator in the validator chain for each required
        atomic property needs to be `not_empty`.
        """
        package_plugin = lib_plugins.lookup_package_plugin()
        schema = package_plugin.create_package_schema()
        for prop in TestSchemaGeneration.required_atomics:
            validator_chain = schema[prop]
            assert validator_chain[0] is toolkit.get_validator('not_empty')

    def test_nonrequired_properties_have_ignore_missing(self):
        """
        The first validator in the validator chain for each required
        atomic property needs to be `not_empty`.
        """
        package_plugin = lib_plugins.lookup_package_plugin()
        schema = package_plugin.create_package_schema()
        for prop in TestSchemaGeneration.nonrequired_atomics:
            validator_chain = schema[prop]
            assert validator_chain[0] is toolkit.get_validator('ignore_missing')

    def test_validation_passes_sanity_check(self):
        """
        Do a sanity check of validation.

        - Does it run at all?
        - Are missing properties marked as missing?
        - Are invalid dates marked as such?
        - Is an invalid license_ids marked as such?
        - Is an invalid geographical_coverage marked as such?
        - Is an invalid geographical_granularity marked as such?
        - Is an invalid temporal_granularity marked as such?
        - Non-standard properties in the data are turned into extras.
        """
        package_plugin = lib_plugins.lookup_package_plugin()
        schema = package_plugin.create_package_schema()
        data = {
            'name': 'foo_bar' ,
            'title': 'Foo Bar' ,
            'date_released': 'foo' ,
            'temporal_coverage_to': '1855-13-06' ,
            'license_id': 'unlicensed' ,
            'temporal_granularity': 'foo' ,
            'geographical_coverage': 'Hamburg' ,
            'geographical_granularity': 'Atom',
            'data_anonymized': 4,
        }
        mock_model = mock.MagicMock()
        mock_session = mock_model.session
        context = {'model': mock_model, 'session': mock_session}
        converted_data, errors_unflattened = df.validate(data, schema, context)
        missing = [
            'berlin_type',
            'maintainer_email',
            'author',
            'notes',
            'berlin_source'
        ]
        bad_date = ['date_released', 'temporal_coverage_to']
        for prop in missing:
            assert errors_unflattened[prop] == ['Missing value']
        for prop in bad_date:
            assert errors_unflattened[prop] == ['Date format incorrect. Use ISO8601: YYYY-MM-DD.']
        assert 'license_id' in errors_unflattened
        assert 'temporal_granularity' in errors_unflattened
        assert 'geographical_granularity' in errors_unflattened
        assert 'geographical_coverage' in errors_unflattened
        assert 'data_anonymized' in errors_unflattened

        flat_extras = {}
        for extra in converted_data['extras']:
            key = extra['key']
            flat_extras[key] = extra['value']

        for key, value in flat_extras.items():
            assert value is data[key]

    def setup_group(self, _name):
        return factories.Group(name=_name)

    def setup_user(self):
        return factories.User()

    def link_user_to_group(self, user, group):
        helpers.call_action(
            'member_create',
            id=group['id'],
            object=user['id'],
            object_type='user',
            capacity='editor'
        )

    def generate_context(self, user):
        mock_model = mock.MagicMock()
        mock_session = mock_model.session
        return {
            'model': mock_model ,
            'session': mock_session ,
            'user': user['name']
        }


    def test_no_category_generates_error(self):
        """
        The input to Berlin_Dataset_SchemaPlugin.validate() must contain a
        `category` attribute or a `groups` attribute.
        """
        package_plugin = lib_plugins.lookup_package_plugin()
        schema = package_plugin.create_package_schema()

        helpers.reset_db()
        user = self.setup_user()

        data = {
            'name': 'foo_bar' ,
            'title': 'Foo Bar' ,
        }
        context = self.generate_context(user)
        validated_data = package_plugin.validate(context, data, schema, "package_create")

        _data = validated_data[0]
        _errors = validated_data[1]
        assert _errors['groups'] == ["Required field 'groups' not set."]

    def test_template_category_becomes_group(self):
        """
        If the input to Berlin_Dataset_SchemaPlugin.validate() contains a
        `category` attribute, it is turned into a group in `groups`.
        """
        package_plugin = lib_plugins.lookup_package_plugin()
        schema = package_plugin.create_package_schema()

        helpers.reset_db()
        group = self.setup_group('arbeit')
        user = self.setup_user()
        self.link_user_to_group(user, group)        

        data = {
            'name': 'foo_bar' ,
            'title': 'Foo Bar' ,
            'category': group['name']
        }
        context = { 'user': user['name'] }
        users_groups = get_action('group_list_authz')(context, {})
        validated_data = package_plugin.validate(context, data, schema, "package_create")

        _data = validated_data[0]
        _errors = validated_data[1]
        assert _data['groups'] == [ { 'name': group['name'] } ]
        assert 'groups' not in _errors

    def test_nonexistant_category_generates_error(self):
        """
        Only existing groups can be chosen as a category.
        """
        package_plugin = lib_plugins.lookup_package_plugin()
        schema = package_plugin.create_package_schema()

        helpers.reset_db()
        user = self.setup_user()

        data = {
            'name': 'foo_bar' ,
            'title': 'Foo Bar' ,
            'category': 'arbeit'
        }
        context = { 'user': user['name'] }
        validated_data = package_plugin.validate(context, data, schema, "package_create")

        _data = validated_data[0]
        _errors = validated_data[1]

        assert 'groups' in _errors

    def test_unauthorized_user_cannot_add_category(self):
        """
        Only users that are members of a group can add it as a category to the dataset.
        I.e., group exists, but user is not a member.
        """
        package_plugin = lib_plugins.lookup_package_plugin()
        schema = package_plugin.create_package_schema()

        helpers.reset_db()
        user = self.setup_user()
        group = self.setup_group('arbeit')

        data = {
            'name': 'foo_bar' ,
            'title': 'Foo Bar' ,
            'category': group['name']
        }
        context = { 'user': user['name'] }
        validated_data = package_plugin.validate(context, data, schema, "package_create")

        _data = validated_data[0]
        _errors = validated_data[1]

        assert 'groups' in _errors

@pytest.mark.ckan_config('ckan.plugins', f"{PLUGIN_NAME}")
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestFacets(object):

    def test_facets_visible(self, app):
        '''Sanity test to see if custom facets are exposed in search page.'''
        dataset_index_url = url_for("dataset.search")
        response = app.get(
            url=dataset_index_url,
            status=200
        )
        # TODO: We should use a more robust test, which really looks at the right
        # place in the markup. Otherwise we might get false positives.
        assert "Geografische Abdeckung" in response.body
        assert "Zeitliche Granularität" in response.body
        # 'Organisation' should only be visible to admins
        assert "Organisation" not in response.body

    def test_facets_visible_admin(self, app):
        '''Sanity test to see if special custom facets are exposed to admins in the search page.'''
        admin_user = factories.Sysadmin(name='theadmin')
        dataset_index_url = url_for("dataset.search")
        response = app.get(
            url=dataset_index_url,
            extra_environ={'Authorization': admin_user['apikey']},
            status=200
        )
        # TODO: We should use a more robust test, which really looks at the right
        # place in the markup. Otherwise we might get false positives.
        assert "Geografische Abdeckung" in response.body
        assert "Zeitliche Granularität" in response.body
        # 'Organisation' should only be visible to admins
        assert "Organisation" in response.body


@pytest.fixture
def user():
    '''Fixture to create a logged-in user.'''
    user = model.User(name="vera_musterer", password=u"testtest")
    model.Session.add(user)
    model.Session.commit()
    return user

@pytest.mark.ckan_config('ckan.plugins', f"{PLUGIN_NAME}")
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestPlugin(object):

    def test_schema_route_logged_in(self, app, user):
        '''Test rendering of schema for a logged-in user.'''
        response = app.get(
            headers=[("Authorization", user.apikey)],
            url="/schema",
            status=200
        )
        assert "Schema" in response.body

    def test_schema_route_non_logged_in(self, app):
        '''Test rendering of schema for a non logged-in user.'''
        response = app.get(
            url="/schema",
            status=200
        )
        assert "Schema" in response.body
