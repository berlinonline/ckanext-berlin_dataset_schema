# Custom SOLR Schema

This folder contains a customised version of the [standard CKAN SOLR schema](https://raw.githubusercontent.com/ckan/ckan/master/ckan/config/solr/schema.xml).
The custom schema introduces the new `author_string` field, which allows to use tha package author as a facet.

Copy this file rather than the standard schema when installing CKAN.