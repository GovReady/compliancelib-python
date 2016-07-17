#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Class for OpenControl

Instantiate and then...

Load an OpenControl component YAML file (e.g., https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml).

Methods provide information about the Security Control.

Visit [tbd] for the latest version.

Example python CLI

import sys
import compliancelib
# Identify a couple OpenControl files to import
# Eventually, this should be from reading an opencontrol.yaml file
f1 = 'https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml'
f2 = 'https://raw.githubusercontent.com/opencontrol/cf-compliance/master/UAA/component.yaml'

# instantiate an OpenControl object to hold an array of controls
oc = compliancelib.OpenControl()

# load file 1
oc.load_ocfile_from_url(f1)
# load file 1
oc.load_ocfile_from_url(f2)

# look at keys, which for now is file names
# in future probably should be component names
oc.ocfiles.keys()
oc.ocfiles[f1]

# loop though what controls are statisfied by second `f2` OpenControl YAML file
# demonstrate combining OpenControl content with ComplianceLib content
for c in oc.ocfiles[f2]['satisfies']: 
  try:
    cd = compliancelib.NIST800_53(c['control_key'])
    if c['implementation_status'] == 'none':
      # putting implementation status into SSP terminology
      status = 'planned'
    else:
      status = c['implementation_status']
    print "%s - %s - %s" % (c['control_key'], status, cd.title)
    # print cd.description
  except:
    print "%s - Error %s" % (c['control_key'], sys.exc_info()[0])

for c in oc.ocfiles[f2]['satisfies']: 
    print c['control_key']
    cd = compliancelib.NIST800_53(c['control_key'])
    print cd.title

# If we build an index of control_keys, then we can look up control details easily,
# but we have to remember that a control_key can be in more than one component file

cks2 = {}
for kf in oc.ocfiles.keys():
  print kf
  for c in oc.ocfiles[kf]['satisfies']:
    if c['control_key'] not in cks2:
      cks2[c['control_key']] = {kf: c}
    else:
      cks2[c['control_key']].append({kf: c})

# let's start with a control and look up implementation
x = "AC-7"
sc = compliancelib.NIST800_53(x)
sc.title
cks[sc.id]
cks2[sc.id]
# oc.ocfiles[cks[sc.id]]['satisfies']
cks2[sc.id][f2]['narrative'][0]['text']
cks2[sc.id][f2]
"""

__author__ = "Greg Elin (gregelin@govready.com)"
__version__ = "$Revision: 0.0.1 $"
__date__ = "$Date: 2016/07/13 19:50:00 $"
__copyright__ = "Copyright (c) 2015 GovReady PBC"
__license__ = "Apache Software License 2.0"

import os
import json
import yaml
import re
import urllib2
import sys

class OpenControl():
    "initialize OpenControl security controls implementation"
    def __init__(self):
        self.ocfiles = {}
        self.dummy_func()
        # define the dictionaries we will support so we avoid unexpected data
        self.supported_dictionaries = ['components', 'standards', 'certifications', 'roles']
        # stub out a system
        self._stub_system()
        pass

    def dummy_func(self):
        "blah"
        c = 3
        return c

    def load_ocfile_from_url(self, ocfileurl):
        "load OpenControl component YAML file from URL"
        # file must be actual YAML file
        # do not load if url already loaded
        if ocfileurl in self.ocfiles.keys():
            return
        # load OpenControl file
        try:
            self.ocfiles[ocfileurl] = yaml.safe_load(urllib2.urlopen(ocfileurl))
        except:
            print("Unexpected error loading YAML file:", sys.exc_info()[0])
            raise

    # load stubs
    def _stub_system(self):
      # To do, load system information file
      self.system = {}
      self.system['name'] = "Test System"
      self.system['components'] = {}
      self.system['certifications'] = {}
      self.system['standards'] = {}
      self.system['roles'] = {}

    def system_component_add(self, component_name, component_dict):
      "add a component as a dictionary to the system with the component name as key"
      self.system['components'][component_name] = component_dict

    def system_component_add_from_url(self, oc_componentyaml_url):
      "add a component as a dictionary to the system from an OpenControl YAML file at a URL"
      # go load opencontrol file
      try:
        my_dict = yaml.safe_load(urllib2.urlopen(oc_componentyaml_url))
        # todo - add checks to make sure it is a proper opencontrol file
      except:
        print("Unexpected error loading YAML file:", sys.exc_info()[0])
        my_dict = None
        raise
      if (my_dict):
        self.system_component_add(my_dict['name'], my_dict)

    def system_component_list(self):
      "list the components composing the system as array"
      return self.system['components'].keys()

    # generic method for loading dictionaries
    def system_dict_add(self, my_dict_type, my_dict_name, my_dict):
      "load a dictionary into system object"
      if my_dict_type in self.supported_dictionaries:
        # to do - validate dictionary
        if (my_dict and my_dict_name):
          self.system[my_dict_type][my_dict_name] = my_dict
      else:
        # pass or indicate error
        raise Exception('Attempt to load unsupported dictionary type %s' % my_dict_type)

    def system_dict_add_from_url(self, dict_type, url):
      "load a dictionary into system object from a URL"
      if dict_type in self.supported_dictionaries:
        try:
          my_dict = yaml.safe_load(urllib2.urlopen(url))
          # todo - validate proper opencontrol file
        except:
          print("Unexpected error loading YAML file:", sys.exc_info()[0])
          my_dict = None
          raise
        if (my_dict):
          self.system[dict_type][my_dict[name]] = my_dict
      else:
        raise Exception('Attempt to load unsupported dictionary type %s' % dict_type)

    def system_standard_list(self):
      "list the standards composing the system as array"
      return self.system['standards'].keys()

    def system_certification_list(self):
      "list the certifications composing the system as array"
      return self.system['certifications'].keys()

    def system_role_list(self):
      "list the roles composing the system as array"
      return self.system['roles'].keys()

    def system_compliance_profile_abstract(self):
      "dump high level system compliance profile abstract"
      scpa = {"name" :  self.system['name'],
        "components" : self.system['components'].keys(),
        "stanards" : self.system['standards'].keys(),
        "certifications" : self.system['certifications'].keys()}
      return scpa
