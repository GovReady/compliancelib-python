#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Class for OpenControl Files

Read OpenControl Files

Read various OpenControl YAML file formats:
- opencontrol.yaml
- component.yaml
(etc)


Example python CLI

import sys, yaml, pprint

import compliancelib
# instantiate an OpenControlFiles object
sp = compliancelib.OpenControlFiles()

# transforming opencontrol component urls

def resolve_component_url(repo_url, revision, path, yaml_file = 'component.yaml'):
  "Resolve url of github repo to actual opencontrol detail yaml file"
  # TODO Sanitize path components better
  ocfile_url = ''
  if 'https://github.com/' in repo_url:
    repo_service = 'github'
  if (repo_service == 'github'):
    ocfile_url = "%s/%s/%s/%s" % (repo_url.replace('https://github.com/','https://raw.githubusercontent.com/'), revision, path, yaml_file)
  return ocfile_url

resolve_component_url('https://github.com/18F/cg-compliance','master','./CloudCheckr')
# https://raw.githubusercontent.com/18F/cg-compliance/master/./CloudCheckr/component.yaml



"""

__author__ = "Greg Elin (gregelin@govready.com)"
__version__ = "$Revision: 0.1.0 $"
__date__ = "$Date: 2016/07/20 07:27:00 $"
__copyright__ = "Copyright (c) 2016 GovReady PBC"
__license__ = "Apache Software License 2.0"

import os
import json
import yaml
import re
import urllib2
import sys

class OpenControlFiles():
    "initialize OpenControlFiles object"
    def __init__(self):
        self.ocfiles = {}

    # Not using this method anymore, worth keeping around?
    def load_ocfile_from_url(self, ocfileurl):
        "load OpenControl component YAML file from URL"
        # file must be actual YAML file
        # idempotent loading - do not load if url already loaded
        if ocfileurl in self.ocfiles.keys():
            return
        try:
            self.ocfiles[ocfileurl] = yaml.safe_load(urllib2.urlopen(ocfileurl))
        except:
            print("Unexpected error loading YAML file:", sys.exc_info()[0])
            raise

    def resolve_component_url(self, repo_url, revision, path, yaml_file = 'component.yaml'):
        "Resolve url of github repo to actual opencontrol detail yaml file"
        # TODO Sanitize path components better
        ocfile_url = ''
        if 'https://github.com/' in repo_url:
          repo_service = 'github'
        if (repo_service == 'github'):
          ocfile_url = "%s/%s/%s/%s" % (repo_url.replace('https://github.com/','https://raw.githubusercontent.com/'), revision, path, yaml_file)
        return ocfile_url



