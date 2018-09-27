.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/berlinonline/ckanext-berlin_dataset_schema.svg?branch=master
    :target: https://travis-ci.org/berlinonline/ckanext-berlin_dataset_schema

=============
ckanext-berlin_dataset_schema
=============

Implementation of IDatasetForm to provide a custom dataset schema for the `Berlin Open Data Portal <https://daten.berlin.de>`_. 

.. Put a description of your extension here:
   What does it do? What features does it have?
   Consider including some screenshots or embedding a video!


------------
Requirements
------------

This plugin has been tested with CKAN 2.7.3.


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.berlin_dataset_schema --cover-inclusive --cover-erase --cover-tests
