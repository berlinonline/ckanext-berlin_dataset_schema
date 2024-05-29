# Changelog

## Development

## [0.3.7](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.3.7)

_(2024-05-29)_

- Add user help text to `tags` in JSON schema.

## [0.3.6](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.3.6)

_(2024-04-25)_

- Add new metadata field `hvd_category` (to link to the category of high-value datasets as defined by the [EU commission implementing regulation 2023/138](https://eur-lex.europa.eu/eli/reg_impl/2023/138/oj?uri=CELEX:32023R0138)).
- Add new metadata field `sample_record` (to link to the matching "Musterdatensatz", see https://www.dcat-ap.de/def/dcatde/2.0/implRules/#verwendung-des-musterdatenkatalogs-fur-kommunen).

## [0.3.5](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.3.5)

_(2024-03-21)_

- Add a new field `preview_image` to schema.
This should be used instead of adding the image directly to the markdown-blob with the dataset description.
Using `preview_image` field is the responsibility of the theme extensions and harvesters (e.g. [ckanext-berlintheme](https://github.com/berlinonline/ckanext-berlintheme), [ckanext-datasetsnippets](https://github.com/berlinonline/ckanext-datasetsnippets), [ckanext-fisbroker](https://github.com/berlinonline/ckanext-fisbroker)).
- Update [JSON schema](https://datenregister.berlin.de/schema/berlin_od_schema.json) and [schema website](https://datenregister.berlin.de/schema/), now at version 2.3.1.
- Change Solr image reference in github CI ([test.yml](.github/workflows/test.yml)) to the new naming scheme according to https://github.com/ckan/ckan-solr.

## [0.3.4](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.3.4)

_(2023-01-24)_

- Add missing `geographical_coverage` values `Köpenick`, `Kreuzberg` and `Treptow`.

## [0.3.3](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.3.3)

_(2023-11-09)_

- Add some user help texts to the JSON schema as `user_help_text` attributes.
- Add static page blueprint to serve `/schema/index.html` under `/schema`.

## [0.3.2](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.3.2)

_(2023-06-14)_

- Add custom licenses list (previously in `ckanext-berlin`).

## [0.3.1](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.3.1)

_(2023-06-13)_

- Add add custom SOLR schema, including new field `author_string` of type `string` (rather than `text_general`), which is needed to include the `author` metadatum in facetted browsing.

## [0.3.0](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.3.0)

_(2023-06-09)_

- Implement the [IFacets](https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IFacets) interface to allow faceted search using the custom dataset schema.

## [0.2.5](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.2.5)

_(2023-05-19)_

- Add `schema` to list of public pages to allow access for anonymous users.
- Define extension's version string in [VERSION](VERSION), make it available as `ckanext.berlin_dataset_schema.__version__` and in [setup.py](setup.py).

## [0.2.4](https://github.com/berlinonline/ckanext-berlin_dataset_schema/releases/tag/0.2.4)

_(2023-01-22)_

- Fix `MANIFEST.in`.

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