# coding: utf-8
"""Tests for validation.py."""

import logging
from datetime import datetime
import pytest
import ckan.lib.navl.dictization_functions as df
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
from ckanext.berlin_dataset_schema.validation import Validator

log = logging.getLogger(__name__)

class TestIsodateNotime:
    """
    Tests for validation.isodate_notime() validator.
    """

    def setup(self):
        self.validator = Validator()

    def test_isodate_notime_empty_is_none(self):
        assert self.validator.isodate_notime('') is None

    def test_isodate_notime_datetime_object_is_truncated(self):    
        assert self.validator.isodate_notime(datetime(1969, 9, 6, 7, 43, 23, 10)) == "1969-09-06"

    def test_isodate_notime_datetime_string_is_truncated(self):
        assert self.validator.isodate_notime("1969-09-06T07:43:23.10") == "1969-09-06"

    def test_isodate_notime_illegal_string_after_date_is_ignored(self):
        assert self.validator.isodate_notime("1969-09-06foo bar") == "1969-09-06"

    def test_isodate_notime_datetime_illegal_date_string_raises_invalid_error(self):
        with pytest.raises(df.Invalid):
            self.validator.isodate_notime("foor bar")

# -------------------

class TestIsValidUrl:
    """
    Tests for validation.is_berlin_type() validator.
    """

    def setup(self):
        self.validator = Validator()

    def test_valid_urls_are_accepted(self):
        urls = [
            "http://www.test.org" ,
            "https://www.berlin.de/sen/wirtschaft/wirtschaft/konjunktur-und-statistik/wirtschaftsdaten/" ,
            "https://daten.berlin.de/ref/geo/coverage" ,
            "ftp://an.ftp.site" ,
            "" # empty URL is valid (robustness, etc.)
        ]
        for url in urls:
            assert self.validator.is_valid_url(url) == url

    @pytest.mark.parametrize("url", [
        "noscheme",
        " https://www.berlin.de/sen/wirtschaft/wirtschaft/konjunktur-und-statistik/wirtschaftsdaten/",  # trailing whitespace
        "https://www.berlin.de/ sen/ wirtschaft/",  # internal whitespace
        "foonz://www.berlin.de",  # unknown/invalid scheme
        "https://www.berlin.de/sen/wirtschaft/  ",  # trailing whitespace
    ])
    def test_reject_invalid_url(self, url):
        with pytest.raises(df.Invalid):
            self.validator.is_valid_url(url)

# -------------------

class TestIsBerlinType:
    """
    Tests for validation.is_berlin_type() validator.
    """

    def setup(self):
        self.validator = Validator()

    def test_is_berlin_type_raises_invalid_error_for_bad_value(self):
        with pytest.raises(df.Invalid):
            self.validator.is_berlin_type('goo star')

    def test_is_berlin_type_gives_correct_answer(self):
        berlin_types = [ 'datensatz', 'dokument', 'app' ]
        for _type in berlin_types:
            actual = self.validator.is_berlin_type(_type)
            expected = _type
            assert actual is expected, "%s != %s" % ( actual, expected)

# -------------------

class TestIsLicenseId:
    """
    Tests for validation.is_license_id() validator.
    """

    def setup(self):
        self.validator = Validator()

    def test_is_license_id_raises_invalid_error_for_bad_value(self):
        with pytest.raises(df.Invalid):
            self.validator.is_license_id('unlicensed')

    def test_is_license_id_gives_correct_answer(self):
        license_ids = ["cc-by", "cc-by/4.0", "cc-zero", "cc-by-sa", "cc-by-nc", "dl-de-zero-2.0", "dl-de-by-2.0", "odc-odbl", "other-closed" ]
        for _id in license_ids:
            actual = self.validator.is_license_id(_id)
            expected = _id
            assert actual is expected, "%s != %s" % ( actual, expected)

# -------------------

class TestIsGeoFeature:
    """
    Tests for validation.is_geo_feature() validator.
    """

    def setup(self):
        self.validator = Validator()

    def test_is_geo_feature_raises_invalid_error_for_bad_value(self):
        with pytest.raises(df.Invalid):
            self.validator.is_geo_feature('Hamburg')

    def test_is_geo_feature_gives_correct_answer(self):
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
            actual = self.validator.is_geo_feature(_feature)
            expected = _feature
            assert actual is expected, "%s != %s" % ( actual, expected)

# -------------------

class TestIsGeoGranularity:
    """
    Tests for validation.is_geo_granularity() validator.
    """

    def setup(self):
        self.validator = Validator()

    def test_is_geo_granularity_raises_invalid_error_for_bad_value(self):
        with pytest.raises(df.Invalid):
            self.validator.is_geo_granularity('Dumdum')

    def test_is_geo_granularity_gives_correct_answer(self):
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
            actual = self.validator.is_geo_granularity(_granularity)
            expected = _granularity
            assert actual is expected, "%s != %s" % ( actual, expected)

# -------------------

class TestIsTemporalGranularity:
    """
    Tests for validation.is_temporal_granularity() validator.
    """

    def setup(self):
        self.validator = Validator()

    def test_is_temporal_granularity_raises_invalid_error_for_bad_value(self):
        with pytest.raises(df.Invalid):
            self.validator.is_temporal_granularity('Dumdum')

    def test_is_temporal_granularity_gives_correct_answer(self):
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
            actual = self.validator.is_temporal_granularity(_granularity)
            expected = _granularity
            assert actual is expected, "%s != %s" % ( actual, expected)

# -------------------

class TestIsInEnum:
    """
    Tests for validation.is_in_enum() helper (mostly covered by other test classes).
    """

    def setup(self):
        self.validator = Validator()

    def test_is_in_enum_valuespace_must_be_list(self):
        with pytest.raises(df.Invalid):
            self.validator.is_in_enum('foo', 'bar')


# -------------------

class TestIsGroupNameValid:
    """
    Tests for validation.is_group_name_valid() check.
    """

    def setup(self):
        """
        Set up some groups and a user that is member of some of them, 
        but not others.
        """

        self.validator = Validator()
        helpers.reset_db()
        self.groups = []
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
        self.restricted_groups = []
        restricted_group_names = [
            u'wirtschaft',
            u'wohnen',
        ]
        for group_name in restricted_group_names:
            self.restricted_groups.append(factories.Group(name=group_name))

    def test_empty_is_an_invalid_group_name(self):
        """
        Group names that don't exist should be invalid.
        """
        context = { 'user': self.user['name'] }
        with pytest.raises(df.Invalid):
            self.validator.is_group_name_valid('empty', context)

    def test_group_names_are_valid_group_names(self):
        """
        Group names that exist and of which the user is a member should be valid.
        """
        context = { 'user': self.user['name'] }
        for group in self.groups:
            assert self.validator.is_group_name_valid(group['name'], context) is group['name']

    def test_restricted_group_is_invalid(self):
        """
        Group names that exist but of which the user is not a member should be invalid.
        """
        context = { 'user': self.user['name'] }
        for group in self.restricted_groups:
            result = True
            try:
                self.validator.is_group_name_valid(group['name'], context)
            except df.Invalid:
                result = False
            assert result is False

