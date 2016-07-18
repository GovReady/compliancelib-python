#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Class for OpenControl

Instantiate and then...

Load an OpenControl component YAML file (e.g., https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml).

Methods provide information about the Security Control.

Visit [tbd] for the latest version.

Example python CLI

import sys, yaml, pprint

import compliancelib
# instantiate an SystemCompliance object
sp = compliancelib.SystemCompliance()

# change name
sp.system['name'] = "GovReady WordPress Dashboard"

# Idempotent adding components from URLs
sp.components()
f1 = 'https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml'
f2 = 'https://raw.githubusercontent.com/opencontrol/cf-compliance/master/UAA/component.yaml'
sp.add_component_from_url(f1)
sp.add_component_from_url(f2)
sp.add_component_from_url(f2)
sp.components()
# Alternatively
sp.add_system_dict_from_url('components', f1)
sp.add_system_dict_from_url('components', f2)
sp.components()
# result
# ['Audit Policy', 'User Account and Authentication (UAA) Server']

# display summary info
sp.summary()
# result
# {'stanards': [], 'certifications': [], 'name': 'GovReady WordPress Dashboard', 'components': ['Audit Policy', 'User Account and Authentication (UAA) Server']}
pprint.pprint(sp.summary())
# result
# {'certifications': [],
# 'components': ['Audit Policy',
#                'User Account and Authentication (UAA) Server'],
# 'name': 'GovReady WordPress Dashboard',
# 'stanards': []}

# query cntrol
ck = "AC-4"
ci = sp.control(ck)
ci.components
ci.components_dict
ci.implementation_narrative


# Test loading GovCloud OpenControl component yaml directly
component_list = ['AC_Policy','AT_Policy','AU_Policy','CA_Policy','CICloudGov','CM_Policy','CP_Policy','CloudCheckr','ELKStack','IA_Policy','IR_Policy','JumpBox','MA_Policy','MP_Policy','PE_Policy','PL_Policy','PS_Policy','RA_Policy','SA_Policy','SC_Policy','SI_Policy','SecureProxy']
urls = ["https://raw.githubusercontent.com/18F/cg-compliance/master/%s/component.yaml" % comp for comp in component_list]
for compurl in urls:
  sp.add_component_from_url(compurl)

# nice controls to test: AU-1, AU-5, SC-10

# Print out control details
ck = "AC-2 (1)"
ci = sp.control(ck)
ci.components
ci.components_dict
ci.implementation_narrative

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
from .nist800_53 import NIST800_53

class SystemCompliance():
    "initialize SystemCompliance security controls implementation"
    def __init__(self):
        self.ocfiles = {}
        # define the dictionaries we will support so we avoid unexpected data
        self.supported_dictionaries = ['components', 'standards', 'certifications', 'assignments', 'roles']
        # stub out a system
        self._stub_system()
        pass

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

    def _stub_system(self):
      # Load a stub file of the sytem
      self.system = {}
      self.system['name'] = "Test System"
      self.system['components'] = {}
      self.system['certifications'] = {}
      self.system['standards'] = {}
      self.system['assignments'] = {}
      self.system['roles'] = {}

    def system_component_add(self, component_name, component_dict):
      "add a component as a dictionary to the system with the component name as key"
      self.system['components'][component_name] = component_dict

    def add_component_from_url(self, oc_componentyaml_url):
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

    def components(self):
      "list the components composing the system as array"
      return self.system['components'].keys()

    # generic method for loading dictionaries
    def add_system_dict(self, my_dict_type, my_dict_name, my_dict):
      "load a dictionary into system object"
      if my_dict_type in self.supported_dictionaries:
        # to do - validate dictionary
        if (my_dict and my_dict_name):
          self.system[my_dict_type][my_dict_name] = my_dict
      else:
        # pass or indicate error
        raise Exception('Attempt to load unsupported dictionary type %s' % my_dict_type)

    def add_system_dict_from_url(self, dict_type, url):
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
          self.system[dict_type][my_dict['name']] = my_dict
      else:
        raise Exception('Attempt to load unsupported dictionary type %s' % dict_type)

    def standards(self):
      "list the standards composing the system as array"
      return self.system['standards'].keys()

    def certifications(self):
      "list the certifications composing the system as array"
      return self.system['certifications'].keys()

    def roles(self):
      "list the roles composing the system as array"
      return self.system['roles'].keys()

    def summary(self):
      "dump high level system compliance profile abstract"
      scpa = {"name" :  self.system['name'],
        "components" : self.system['components'].keys(),
        "standards" : self.system['standards'].keys(),
        "certifications" : self.system['certifications'].keys()}
      return scpa

    def control(self, cid, standard = 'NIST800_53'):
      "create a control object for system combining control info from standard and implementation details"
      # raise error if components are not loaded
      if len(self.components()) < 1:
        raise Exception ("No controls available. No components have been loaded.")

      # create control object from standard (NOTE: only support NIST 800-53 currently)
      if (standard == 'NIST800_53'):
        ci = NIST800_53(cid)
      else:
        raise Exception ("The standard %s is not currently supported." % standard)

      # find all components with content regarding control_key
      # add dictionary of components attribute to control
      ci.components_dict = {}
      for component in self.components():
        component_control_info = [ck for ck in self.system['components'][component]['satisfies'] if ck['control_key'] == cid]
        if (len(component_control_info)) > 0:
          ci.components_dict[component] = component_control_info

      # make it easy to look at list of components related to control by getting list of keys that are names of components
      ci.components = ci.components_dict.keys()

      # determine roles
      ci.roles = {}

      # determine assignments
      ci.assignments = {}

      # determine narrative
      ci.implementation_narrative = ""
      ctl_str = ""
      for component in ci.components:
        # print component
        comp_contribution  = ci.components_dict[component][0]
        for text_item in comp_contribution['narrative']:
          key = ""
          text = ""
          if 'key' in text_item:
            key = "%s:\n" % text_item['key']
          if 'text' in text_item:
            text = text_item['text']
          ctl_str += "%s\nvia %s\n%s\n" % (key, component, text)
      ci.narrative = ctl_str

      # determine implementation status
      ci.implementation_status = ""
      ci.implementation_status_details = {}
      # if all components implemented, then implemented
      # if some components implemented, then partially implemented

      # determine validation
      ci.validation = {}

      # return the control implementation object
      return ci
