#! /bin/bash
nosetests -s --ckan --with-pylons=test.ini --with-coverage --cover-package=ckanext.berlin_dataset_schema --cover-inclusive --cover-erase --cover-html ckanext/berlin_dataset_schema/tests/
