# coding: utf-8
"""Tests for validation.py."""

import logging
from datetime import datetime

import ckan.lib.navl.dictization_functions as df
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import pytest
from ckan.tests.pytest_ckan.fixtures import reset_db

from ckanext.berlin_dataset_schema.validation import Validator

LOG = logging.getLogger(__name__)

@pytest.fixture
def validator() -> Validator:
    return Validator()

@pytest.fixture
def groups(reset_db):
    reset_db()
    groups = []
    group_names = [
        u'arbeit',
        u'bildung',
        u'demographie',
        u'erholung',
        u'geo',
        u'verkehr',
        u'verwaltung',
        u'wahl',
    ]
    for group_name in group_names:
        groups.append(factories.Group(name=group_name))
    return groups

@pytest.fixture
def user(groups):
    user = factories.User()
    for group in groups:
        helpers.call_action(
            'member_create',
            id=group['id'],
            object=user['id'],
            object_type='user',
            capacity='editor'
        )
    return user

@pytest.fixture
def restricted_groups(groups):
    restricted_groups = []
    restricted_group_names = [
        u'wirtschaft',
        u'wohnen',
    ]
    for group_name in restricted_group_names:
        restricted_groups.append(factories.Group(name=group_name))
    return restricted_groups


class TestIsodateNotime:
    """
    Tests for validation.isodate_notime() validator.
    """

    def test_isodate_notime_empty_is_none(self, validator):
        assert validator.isodate_notime('') is None

    def test_isodate_notime_datetime_object_is_truncated(self, validator):
        assert validator.isodate_notime(datetime(1969, 9, 6, 7, 43, 23, 10)) == "1969-09-06"

    def test_isodate_notime_datetime_string_is_truncated(self, validator):
        assert validator.isodate_notime("1969-09-06T07:43:23.10") == "1969-09-06"

    def test_isodate_notime_illegal_string_after_date_is_ignored(self, validator):
        assert validator.isodate_notime("1969-09-06foo bar") == "1969-09-06"

    def test_isodate_notime_datetime_illegal_date_string_raises_invalid_error(self, validator):
        with pytest.raises(df.Invalid):
            validator.isodate_notime("foor bar")

# -------------------

class TestIsValidUrl:
    """
    Tests for validation.is_berlin_type() validator.
    """

    def test_valid_urls_are_accepted(self, validator):
        urls = [
            "http://www.test.org" ,
            "https://www.berlin.de/sen/wirtschaft/wirtschaft/konjunktur-und-statistik/wirtschaftsdaten/" ,
            "https://daten.berlin.de/ref/geo/coverage" ,
            "ftp://an.ftp.site" ,
            "" # empty URL is valid (robustness, etc.)
        ]
        for url in urls:
            assert validator.is_valid_url(url) == url

    @pytest.mark.parametrize("url", [
        "noscheme",
        " https://www.berlin.de/sen/wirtschaft/wirtschaft/konjunktur-und-statistik/wirtschaftsdaten/",  # trailing whitespace
        "https://www.berlin.de/ sen/ wirtschaft/",  # internal whitespace
        "foonz://www.berlin.de",  # unknown/invalid scheme
        "https://www.berlin.de/sen/wirtschaft/  ",  # trailing whitespace
    ])
    def test_reject_invalid_url(self, url, validator):
        with pytest.raises(df.Invalid):
            validator.is_valid_url(url)

# -------------------

class TestIsBerlinType:
    """
    Tests for validation.is_berlin_type() validator.
    """

    def test_is_berlin_type_raises_invalid_error_for_bad_value(self, validator):
        with pytest.raises(df.Invalid):
            validator.is_berlin_type('goo star')

    def test_is_berlin_type_gives_correct_answer(self, validator):
        berlin_types = [ 'datensatz', 'dokument', 'app' ]
        for _type in berlin_types:
            actual = validator.is_berlin_type(_type)
            expected = _type
            assert actual is expected, "%s != %s" % ( actual, expected)

# -------------------

class TestIsLicenseId:
    """
    Tests for validation.is_license_id() validator.
    """

    def test_is_license_id_raises_invalid_error_for_bad_value(self, validator):
        with pytest.raises(df.Invalid):
            validator.is_license_id('unlicensed')

    def test_is_license_id_gives_correct_answer(self, validator):
        license_ids = ["cc-by", "cc-by/4.0", "cc-zero", "cc-by-sa", "cc-by-nc", "dl-de-zero-2.0", "dl-de-by-2.0", "odc-odbl", "other-closed" ]
        for _id in license_ids:
            actual = validator.is_license_id(_id)
            expected = _id
            assert actual is expected, "%s != %s" % ( actual, expected)

# -------------------

class TestIsGeoFeature:
    """
    Tests for validation.is_geo_feature() validator.
    """

    def test_is_geo_feature_raises_invalid_error_for_bad_value(self, validator):
        with pytest.raises(df.Invalid):
            validator.is_geo_feature('Hamburg')

    def test_is_geo_feature_gives_correct_answer(self, validator):
        geo_features = [
            u'Keine',
            u'Adlershof',
            u'Grünau',
            u'Märkisches Viertel',
            u'Müggelheim',
            u'Neu-Hohenschönhausen',
            u'Neukölln',
            u'Niederschöneweide',
            u'Nikolassee',
            u'Weißensee',
        ]
        for _feature in geo_features:
            actual = validator.is_geo_feature(_feature)
            expected = _feature
            assert actual is expected, "%s != %s" % ( actual, expected)

# -------------------

class TestIsGeoGranularity:
    """
    Tests for validation.is_geo_granularity() validator.
    """

    def test_is_geo_granularity_raises_invalid_error_for_bad_value(self, validator):
        with pytest.raises(df.Invalid):
            validator.is_geo_granularity('Dumdum')

    def test_is_geo_granularity_gives_correct_answer(self, validator):
        geo_granularities = [
            'Keine',
            'Deutschland',
            'Berlin',
            'Bezirk',
            'Ortsteil',
            'Prognoseraum',
            'Bezirksregion',
            'Planungsraum',
            'Block',
            'Einschulbereich',
            'Kontaktbereich',
            'PLZ',
            'Stimmbezirk',
            'Quartiersmanagement',
            'Wohnanlage',
            'Wahlkreis'
        ]
        for _granularity in geo_granularities:
            actual = validator.is_geo_granularity(_granularity)
            expected = _granularity
            assert actual is expected, "%s != %s" % ( actual, expected)

# -------------------

class TestIsTemporalGranularity:
    """
    Tests for validation.is_temporal_granularity() validator.
    """

    def test_is_temporal_granularity_raises_invalid_error_for_bad_value(self, validator):
        with pytest.raises(df.Invalid):
            validator.is_temporal_granularity('Dumdum')

    def test_is_temporal_granularity_gives_correct_answer(self, validator):
        temporal_granularities = [ 
            'Keine',
            '5 Jahre',
            'Jahr',
            'Quartal',
            'Monat',
            'Woche',
            'Tag',
            'Stunde',
            'Minute',
            'Sekunde'
        ]
        for _granularity in temporal_granularities:
            actual = validator.is_temporal_granularity(_granularity)
            expected = _granularity
            assert actual is expected, "%s != %s" % ( actual, expected)

# -------------------

class TestIsInEnum:
    """
    Tests for validation.is_in_enum() helper (mostly covered by other test classes).
    """

    def test_is_in_enum_valuespace_must_be_list(self, validator):
        with pytest.raises(df.Invalid):
            validator.is_in_enum('foo', 'bar')


# -------------------

class TestIsGroupNameValid:
    """
    Tests for validation.is_group_name_valid() check.
    """

    def test_empty_is_an_invalid_group_name(self, validator, user):
        """
        Group names that don't exist should be invalid.
        """
        context = { 'user': user['name'] }
        with pytest.raises(df.Invalid):
            validator.is_group_name_valid('empty', context)

    def test_group_names_are_valid_group_names(self, validator, groups, user):
        """
        Group names that exist and of which the user is a member should be valid.
        """
        context = { 'user': user['name'] }
        for group in groups:
            assert validator.is_group_name_valid(group['name'], context) is group['name']

    def test_restricted_group_is_invalid(self, validator, restricted_groups, user):
        """
        Group names that exist but of which the user is not a member should be invalid.
        """
        context = { 'user': user['name'] }
        for group in restricted_groups:
            result = True
            try:
                validator.is_group_name_valid(group['name'], context)
            except df.Invalid:
                result = False
            assert result is False


class TestIsSampleRecord:
    """
    Tests for validation.is_sample_record() validator.
    """

    def test_is_sample_record_raises_invalid_error_for_bad_value(self, validator):
        with pytest.raises(df.Invalid):
            validator.is_sample_record('Dumdum')

    def test_is_sample_record_gives_correct_answer(self, validator):
        sample_records = [ 
            'abfallentsorgung',
            'bau/grundstuecksbewertung',
            'bevoelkerungsstruktur/staatsangehoerigkeit',
            'bildung/kindertageseinrichtung/standort',
            'finanzen/haushalt/ausserplanmaessigeAufwendungen',
            'floraUndFauna/flaeche/naturschutzgebiet',
            'raumplanung',
            'wirtschaft/wirtschaftsfoerderung',
            'wirtschaft/wirtschaftsstandort',
        ]
        for _sample_record in sample_records:
            actual = validator.is_sample_record(_sample_record)
            expected = _sample_record
            assert actual is expected, "%s != %s" % ( actual, expected)

class TestIsHVDCategory:
    """
    Tests for validation.is_hvd_category() validator.
    """

    def test_is_hvd_category_raises_invalid_error_for_bad_value(self, validator):
        with pytest.raises(df.Invalid):
            validator.is_hvd_category('Dumdum')

    def test_is_hvd_category_gives_correct_answer(self, validator):
        hvd_categories = [ 
            'c_a9135398',
            'c_e1da4e07',
            'c_164e0bf5',
            'c_ac64a52d',
            'c_b79e35eb',
            'c_dd313021',
        ]
        for _hvd_category in hvd_categories:
            actual = validator.is_hvd_category(_hvd_category)
            expected = _hvd_category
            assert actual is expected, "%s != %s" % ( actual, expected)

class TestIsTrueBoolean:
    """
    Tests for the validation.is_booleanish() validator.
    """

    @pytest.mark.parametrize("bad_value", [
        1,
        3.14,
        None,
        "T",
        0
    ])
    def test_is_booleanish_raises_invalid_error_for_bad_value(self, validator, bad_value):
        with pytest.raises(df.Invalid):
            validator.is_booleanish(bad_value)

    @pytest.mark.parametrize("good_value", [
        { 'in': "true", 'expected': True },
        { 'in': "True", 'expected': True },
        { 'in': "false", 'expected': False },
        { 'in': "False", 'expected': False },
        { 'in': True, 'expected': True },
        { 'in': False, 'expected': False },
    ])
    def test_is_booleanish_gives_correct_answer(self, validator, good_value):
        assert validator.is_booleanish(good_value['in']) == good_value['expected']

class TestPersonalDataSettingsValid:
    """
    Tests for the validation.personal_data_settings_valid() validator
    """

    @pytest.mark.parametrize("personal_data_settings", [
        {
            'data': {
                ('personal_data',): False,
                ('personal_data_exemption',): False,
                ('data_anonymized',): False 
            },
            'expected': None
        },
        {
            'data': {
                ('personal_data',): False,
                ('personal_data_exemption',): True,
                ('data_anonymized',): True 
            },
            'expected': ('personal_data_exemption',)
        },
        {
            'data': {
                ('personal_data',): False,
                ('personal_data_exemption',): False,
                ('data_anonymized',): True 
            },
            'expected': ('data_anonymized',)
        },
        {
            'data': {
                ('personal_data',): False,
                ('personal_data_exemption',): True,
                ('data_anonymized',): False 
            },
            'expected': ('personal_data_exemption',)
        },
        {
            'data': {
                ('personal_data',): True,
                ('personal_data_exemption',): True,
                ('data_anonymized',): True 
            },
            'expected': ('data_anonymized',)
        },
        {
            'data': {
                ('personal_data',): True,
                ('personal_data_exemption',): True,
                ('data_anonymized',): False 
            },
            'expected': None
        },
        {
            'data': {
                ('personal_data',): True,
                ('personal_data_exemption',): False,
                ('data_anonymized',): True 
            },
            'expected': None
        },
        {
            'data': {
                ('personal_data',): True,
                ('personal_data_exemption',): False,
                ('data_anonymized',): False 
            },
            'expected': ('personal_data_exemption',)
        },
        {
            'data': {
                ('personal_data',): True,
                ('personal_data_exemption',): False,
                ('data_anonymized',): False 
            },
            'expected': ('data_anonymized',)
        },
    ])
    def test_personal_data_settings_valid_gives_correct_answer(self, validator: Validator, personal_data_settings):
        errors = {
            ('personal_data',): [],
            ('personal_data_exemption',): [],
            ('data_anonymized',): [],
        }
        validator.personal_data_settings_valid(None, personal_data_settings['data'], errors, None)
        if personal_data_settings['expected']:
            # there must be entries in the error list for the expected field
            assert len(errors[personal_data_settings['expected']]) > 0
        else:
            # all error lists must be empty
            for field, error_list in errors.items():
                assert len(error_list) == 0
