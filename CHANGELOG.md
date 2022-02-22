# Changelog

## Development

## [0.2.3](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.2.3)

_(2022-02-22)_

- Fix codecov configuration and add badge.

## [0.2.2](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.2.2)

_(2022-02-22)_

- Run tests on pushes, but not on pushing tags.

## [0.2.1](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.2.1)

_(2022-02-22)_

- Fix an error in package validation (don't check group membership for `package_show`).

## [0.2.0](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.2.0)

_(2021-11-24)_

- Convert from Python 2 to Python 3.
- Switch testing framework from Nose to Pytest.
- Switch CI from travis to gh-actions.
- Switch from RST to Markdown in README.

## [0.1.3](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.1.3)

_(2019-08-09)_

- Bump schema to [version 2.2](https://github.com/berlinonline/berlin_od_schema/tree/2.2).
- The last version to work with Python 2 / CKAN versions < 2.9.

## [0.1.2](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.1.2)

_(2019-03-18)_

- Bump schema to [version 2.1](https://github.com/berlinonline/berlin_od_schema/tree/2.1).

## [0.1.1](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.1.1)

_(2018-11-06)_

- Plugin now implements [IValidators](https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IValidators) interface to expose the validator functions in [validation.py](ckanext/berlin_dataset_schema/validation.py).

## [0.1.0](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.1.0)

_(2018-10-30)_

- Package validation has been enabled.
    - Validation is based on a JSON schema [`berlin_od_schema.json`](ckanext/berlin_dataset_schema/public/schema/berlin_od_schema.json), which is included in the extension.
    - The schema is loaded and interpreted to drive the validation.
    - Validation includes a way to ensure that at least one group has been set for the package.
- Unit tests have been added with almost complete code coverage.