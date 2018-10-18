# Changelog

## Development

- Package validation has been enabled.
    - Validation is based on a JSON schema [`berlin_od_schema.json`](ckanext/berlin_dataset_schema/public/schema/berlin_od_schema.json), which is included in the extension.
    - The schema is loaded and interpreted to drive the validation.
    - Validation includes a way to ensure that at least one group has been set for the package.
- Unit tests have been added.