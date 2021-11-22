# Changelog

## Development

- Convert from Python 2 to Python 3:
  - Switch testing framework from Nose to Pytest.

## 0.1.3

- Bump schema to [version 2.2](https://github.com/berlinonline/berlin_od_schema/tree/2.2).

## 0.1.2

- Bump schema to [version 2.1](https://github.com/berlinonline/berlin_od_schema/tree/2.1).

## 0.1.1

- Plugin now implements [IValidators](https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IValidators) interface to expose the validator functions in [validation.py](ckanext/berlin_dataset_schema/validation.py).

## 0.1.0

- Package validation has been enabled.
    - Validation is based on a JSON schema [`berlin_od_schema.json`](ckanext/berlin_dataset_schema/public/schema/berlin_od_schema.json), which is included in the extension.
    - The schema is loaded and interpreted to drive the validation.
    - Validation includes a way to ensure that at least one group has been set for the package.
- Unit tests have been added with almost complete code coverage.