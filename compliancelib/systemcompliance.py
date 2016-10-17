#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Class for OpenControl

Instantiate and then...

Load an OpenControl component YAML file (e.g., https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml).

Methods provide information about the Security Control.

Visit [tbd] for the latest version.

LICENSE

ComplianceLib SystemCompliance is a class for representing compliance as code for an information system.
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
------------------

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
ci.implementation_status
ci.assignments
ci.implementation_narrative
print(ci.implementation_narrative)

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
print(ci.implementation_narrative)


# very short, load from opencontrol
import compliancelib
sp = compliancelib.SystemCompliance()
sp.load_system_from_opencontrol_repo('https://github.com/18F/cg-compliance')
sp.control('AC-4').title
print(sp.control('AC-4').description)
print(sp.control('AC-4').implementation_narrative)
print(sp.control('AC-4').implementation_status)
sp.control_ssp_text('AC-4')

# list controls from each component
for component in sp.components():
  print(component)
  [ck['control_key'] for ck in sp.system['components'][component]['satisfies']]

# freedonia-compliance
import compliancelib
sp = compliancelib.SystemCompliance()
sp.load_system_from_opencontrol_repo('https://github.com/opencontrol/freedonia-compliance')
sp.control('AU-1').title
sp.control_ssp_text('AU-1')
print(sp.control('AU-1').description)
print(sp.control('AU-1').implementation_narrative)

for component in sp.components():
  print(component)
  [ck['control_key'] for ck in sp.system['components'][component]['satisfies']]
"""

__author__ = "Greg Elin (gregelin@govready.com)"
__version__ = "$Revision: 1.0.0 $"
__date__ = "$Date: 2016/10/16 23:14:00 $"
__copyright__ = "Copyright (c) 2016 GovReady PBC"
__license__ = "Apache Software License 2.0"

import os
import json
import yaml
import re
import sys
from .nist800_53 import NIST800_53
from .opencontrolfiles import OpenControlFiles

if sys.version_info >= (3, 0):
    from urllib.parse import urlparse
    from urllib.request import urlopen
if sys.version_info < (3, 0) and sys.version_info >= (2, 5):
    from urlparse import urlparse
    from urllib2 import urlopen

class SystemCompliance():
    "initialize SystemCompliance security controls implementation"
    def __init__(self):
        self.ocfiles = {}
        # define the dictionaries we will support so we avoid unexpected data
        self.supported_dictionaries = ['components', 'standards', 'certifications', 'assignments', 'roles']
        # stub out a system
        self._stub_system()
        pass

    def _stub_system(self):
      # Load a stub file of the sytem
      self.system = {}
      self.system['name'] = ""
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
      print("oc_componentyaml_url: ", oc_componentyaml_url)
      try:
        my_dict = yaml.safe_load(urlopen(oc_componentyaml_url))
        # todo - add checks to make sure it is a proper opencontrol file
      except:
        print("Unexpected error loading YAML file:", sys.exc_info()[0])
        my_dict = None
        raise
      if (my_dict):
        # TODO: Consider if method `system_component_add` needed
        self.system_component_add(my_dict['name'], my_dict)

    def components(self):
      "list the components composing the system as array"
      return list(self.system['components'])

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
          my_dict = yaml.safe_load(urlopen(url))
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
      return list(self.system['standards'])

    def certifications(self):
      "list the certifications composing the system as array"
      return list(self.system['certifications'])

    def roles(self):
      "list the roles composing the system as array"
      return list(self.system['roles'])

    def summary(self):
      "dump high level system compliance profile abstract"
      scpa = {"name" :  self.system['name'],
        "components" : list(self.system['components']),
        "standards" : list(self.system['standards']),
        "certifications" : list(self.system['certifications'])}
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
      ci.components = list(ci.components_dict)

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
      ci.implementation_narrative = ctl_str

      # determine implementation status
      # We need a dictionary because mutiple components support a control
      ci.implementation_status_details = {}
      for component in ci.components:
        comp_contribution  = ci.components_dict[component][0]
        ci.implementation_status_details[component] = comp_contribution['implementation_status']
      # now that we have implementation status details for components, calculate actual status
          # From FedRAMP-SSP-Template-High-2016-06-20-v01-00.docx
          # Implementation Status (check all that apply):
          # ☐ Implemented
          # ☐ Partially implemented
          # ☐ Planned
          # ☐ Alternative implementation
          # ☐ Not applicable
      ci.implementation_status = [ci.implementation_status_details[component] for component in list(ci.implementation_status_details)]
      # determine validation
      ci.validation = {}

      # return the control implementation object
      return ci

    def control_ssp_text(self, cid):
      "print out text for a control listing in system security plan (assume NIST800-53)"
      ci = self.control(cid)
      print("%s - %s" % (ci.id, ci.title))
      print("%s" % (ci.description))
      print("\n")
      print("responsible: %s" % ci.responsible)
      print("roles: %s" % ci.roles)
      print("implementation status: %s\n" % ci.implementation_status)
      print("%s" % ci.implementation_narrative)

    def load_system_from_opencontrol_repo(self, repo_url, revision='master', verbose=''):
      "load system details and control implementation from a repo"
      # TODO Reset all values before loading new system
      #TODO handle not finding opencontrol.yaml file in repo
      ocf =  OpenControlFiles()

      item_type = "components"
      for url in ocf.list_items_urls_in_repo(ocf.resolve_ocfile_url(repo_url, revision), item_type):
        if (verbose=='v'):
          print("Reading %s %s" % (item_type, url))
        self.add_component_from_url(url)

      item_type = "standards"
      for url in ocf.list_items_urls_in_repo(ocf.resolve_ocfile_url(repo_url, revision), item_type):
        if (verbose=='v'):
          print("Reading %s %s" % (item_type, url))
        self.add_system_dict_from_url("standards", url)

      item_type = "certifications"
      for url in ocf.list_items_urls_in_repo(ocf.resolve_ocfile_url(repo_url, revision), item_type):
        if (verbose=='v'):
          print("Reading %s %s" % (item_type, url))
        self.add_system_dict_from_url("certifications", url)

      return True

