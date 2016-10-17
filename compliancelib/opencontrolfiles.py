#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Class for OpenControl Files

Read various OpenControl YAML files:
- opencontrol.yaml
- component.yaml
(etc)

LICENSE

ComplianceLib OpenControlFiles is a class for reading OpenControl YAML files
Copyright (C) 2016  GovReady PBC.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Example python CLI
--------------------

import sys, yaml, pprint

import compliancelib
# instantiate an OpenControlFiles object
ocf = compliancelib.OpenControlFiles()

# transforming opencontrol component urls
repo_ref = 'https://github.com/18F/cg-compliance'
revision = 'master'
component_path = ''
ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
print("test: ocfileurl %s" % ocfileurl)
# load components from opencontrol.yaml file
components_urls = ocf.list_items_urls_in_repo(ocfileurl, "components")

# instantiate an SystemCompliance object
sp = compliancelib.SystemCompliance()
for compurl in ocf.list_items_urls_in_repo(ocfileurl, "components"):
  sp.add_component_from_url(compurl)

# Print out control details
ck = "AC-2 (1)"
ci = sp.control(ck)
ci.components
ci.components_dict
print(ci.implementation_narrative)

# shorter
import compliancelib
ocf =  compliancelib.OpenControlFiles()
sp = compliancelib.SystemCompliance()
for url in ocf.list_items_urls_in_repo(ocf.resolve_ocfile_url('https://github.com/18F/cg-compliance','master')):
    sp.add_component_from_url(url)

sp.control('AC-4').title
print(sp.control('AC-4').description)
print(sp.control('AC-4').implementation_narrative)
sp.control_ssp_text('AC-4')

# freedonia-compliance
import compliancelib
sp = compliancelib.SystemCompliance()
sp.load_system_from_opencontrol_repo('https://github.com/opencontrol/freedonia-compliance')
sp.control('AC-4').title
print(sp.control('AC-4').description)
print(sp.control('AC-4').implementation_narrative)
sp.control_ssp_text('AC-4')

# setting logging levels
# opencontrolfiles.py incorporates python logging module
ocf = compliancelib.OpenControlFiles()
ocf.logger.setLevel("DEBUG")

"""

__author__ = "Greg Elin (gregelin@govready.com)"
__version__ = "$Revision: 1.0. $"
__date__ = "$Date: 2016/10/16 10:16:00 $"
__copyright__ = "Copyright (c) 2016 GovReady PBC"
__license__ = "Apache Software License 2.0"

import os
import json
import yaml
import re
import sys
import logging

if sys.version_info >= (3, 0):
    from urllib.parse import urlparse
    from urllib.request import urlopen
if sys.version_info < (3, 0) and sys.version_info >= (2, 5):
    from urlparse import urlparse
    from urllib2 import urlopen

# create logger with 'opencontrolfiles'
logger = logging.getLogger('opencontrolfiles')
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('[LOG compliancelib]; %(levelname)s; %(asctime)s; %(name)s; %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)

class OpenControlFiles():
    "initialize OpenControlFiles object"

    def __init__(self):
        self.ocfiles = {}
        self.logger = logging.getLogger('opencontrolfiles')

    def load_ocfile_from_url(self, ocfileurl):
        "load OpenControl component YAML file from URL"
        # file must be actual YAML file
        # idempotent loading - do not load if url already loaded
        if ocfileurl in self.ocfiles.keys():
            return self.ocfiles[ocfileurl]
        try:
            self.ocfiles[ocfileurl] = yaml.safe_load(urlopen(ocfileurl))
        except:
            print("Unexpected error loading YAML file:", sys.exc_info()[0])
            self.logger.error("Unexpected error loading YAML file:", sys.exc_info()[0])
            raise
        return self.ocfiles[ocfileurl]

    def resolve_ocfile_url(self, repo_url, revision, yaml_file = 'opencontrol.yaml'):
        "Resolve url of github repo to actual opencontrol detail yaml file"
        self.logger.debug("Resolving url of repo_url ({}), revision ({}), yaml_file ({})".format(repo_url, revision, yaml_file))
        # TODO Sanitize path components better
        # TODO use urlparse library
        ocfile_url = ''
        self.logger.debug("repo_url in resolve_ocfile_url: %s" % repo_url)
        # Resolve GitHub repos
        if 'https://github.com/' in repo_url:
            repo_service = 'github'
            ocfile_url = "%s/%s/%s" % (repo_url.replace('https://github.com/','https://raw.githubusercontent.com/'), revision, yaml_file)
            return ocfile_url
        # Resolve localfile repo (`file:///`)
        if 'file:///' in repo_url:
           repo_service = 'localfile'
           ocfile_url = "%s/%s" % (repo_url, yaml_file)
           self.logger.info("opencontrol ocfile_url is {}".format(ocfile_url))
           return ocfile_url
        # TODO: Add non-GitHub services here
        return repo_url

    def resolve_item_url(self, repo_url, revision, path, item_type):
        "Resolve url of github repo to actual opencontrol component.yaml file"
        # TODO Sanitize path components better

        # Resolve GitHub repos
        if 'https://github.com/' in repo_url:
            if (item_type == "components"):
                return "%s/%s/%s/%s" % (repo_url.replace('https://github.com/','https://raw.githubusercontent.com/'), revision, path, "component.yaml")
            elif (item_type == "standards"):
                return "%s/%s/%s" % (repo_url.replace('https://github.com/','https://raw.githubusercontent.com/'), revision, path)
            elif (item_type == "certifications"):
                return "%s/%s/%s" % (repo_url.replace('https://github.com/','https://raw.githubusercontent.com/'), revision, path)
            else:
                raise Exception('Attempt to load unsupported item type service. Only "components", "standards", and "certifications" supported in this version of ComplianceLib')
        # Resolve localfile repo (`file:///`)
        if 'file:///' in repo_url:
            if (item_type == "components"):
                ocfile_url = "%s/%s/%s" % (repo_url, path, "component.yaml")
            elif (item_type == "standards"):
                ocfile_url = "%s/%s" % (repo_url, path)
            elif (item_type == "certifications"):
                ocfile_url = "%s/%s" % (repo_url, path)
            else:
                raise Exception('Attempt to load unsupported item type service. Only "components", "standards", and "certifications" supported in this version of ComplianceLib')
            self.logger.info("component ocfile_url is {}".format(ocfile_url))
            return ocfile_url
        # TODO: Add non-GitHub services here
        # No match of hosted type
        raise Exception('Attempt to load unsupported repo service. Only GitHub.com and local repositories (file:///) supported in this version of ComplianceLib')

    def list_items_in_repo(self, ocfileurl, item_type):
        "list paths of components found in an opencontrol.yaml file, not including any dependencies"
        item_list = []
        ocfile_dict = self.load_ocfile_from_url(ocfileurl)
        if item_type in ocfile_dict.keys():
            item_list = ocfile_dict[item_type]
        return item_list

    def list_items_urls_in_repo(self, ocfileurl, item_type):
        "list item urls found in an opencontrol.yaml file"
        parsed_uri = urlparse(ocfileurl)
        if (parsed_uri.netloc =='raw.githubusercontent.com'):
            repo_service = 'github'
            repo_owner = parsed_uri.path.split('/')[1]
            revision = parsed_uri.path.split('/')[3]
            repo_ref = "%s://%s/%s/%s" % (parsed_uri.scheme, 'github.com', parsed_uri.path.split('/')[1], parsed_uri.path.split('/')[2])
            self.logger.debug("repo_ref in list_items_urls_in_repo: %s" % repo_ref)
            ocfileurl = self.resolve_ocfile_url(repo_ref, revision)
            self.logger.info("ocfileurl: %s" % ocfileurl)
            component_list = self.list_items_in_repo(ocfileurl, item_type)
            components_urls_list = [self.resolve_item_url(repo_ref, revision, component_url, item_type) for component_url in component_list]
            return components_urls_list
        elif (parsed_uri.scheme == 'file') :
            self.logger.info("parsed_uri.scheme == 'file'")
            #urlparse(ocfileurl)
            #ParseResult(scheme='file', netloc='', path='/codedata/code/bunsen-compliance', params='', query='', fragment='')
            self.logger.info(parsed_uri)
            repo_service = 'localfile'
            repo_owner = ''
            revision = 'master'
            # repo_ref = "%s://%s/%s/%s" % (parsed_uri.scheme, 'github.com', parsed_uri.path.split('/')[1], parsed_uri.path.split('/')[2])

            repo_ref = "%s://%s" % (parsed_uri.scheme, parsed_uri.path.split('/opencontrol.yaml')[0])
            self.logger.info("repo_ref in list_components_urls: {}".format(repo_ref))
            ocfileurl = self.resolve_ocfile_url(repo_ref, revision)
            self.logger.info("ocfileurl: %s" % ocfileurl)
            component_list = self.list_items_in_repo(ocfileurl, item_type)
            components_urls_list = [self.resolve_item_url(repo_ref, revision, component_url, item_type) for component_url in component_list]
            return components_urls_list
        else:
            # only GitHub supported
            raise Exception('Attempt to load unsupported repo service. Only GitHub.com and local repositories (file:///)supported in this version of ComplianceLib')


