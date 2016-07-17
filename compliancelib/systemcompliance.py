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
# instantiate an OpenControl object to hold an array of controls
oc = compliancelib.OpenControl()

sp.system['name']
sp.system['name'] = "GovReady WordPress Dashboard"

sp.system_component_list()
# result
# []


# Add components from URLs
f1 = 'https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml'
f2 = 'https://raw.githubusercontent.com/opencontrol/cf-compliance/master/UAA/component.yaml'
sp.system_component_add_from_url(f1)
sp.system_component_add_from_url(f2)

# Alternatively
# and it's idempotent
sp.system_dict_add_from_url('components', f1)
sp.system_dict_add_from_url('components', f2)

sp.system_component_list()
# result
# ['Audit Policy', 'User Account and Authentication (UAA) Server']


sp.system_compliance_profile_abstract()
# {'stanards': [], 'certifications': [], 'name': 'GovReady WordPress Dashboard', 'components': ['Audit Policy', 'User Account and Authentication (UAA) Server']}

import pprint
pprint.pprint(sp.system_compliance_profile_abstract())
{'certifications': [],
 'components': ['Audit Policy',
                'User Account and Authentication (UAA) Server'],
 'name': 'GovReady WordPress Dashboard',
 'stanards': []}

ck = "AC-4"
compliancelib.NIST800_53(ck)
# <compliancelib.nist800_53.NIST800_53 object at 0x100ccc350>

sc_standard_info = compliancelib.NIST800_53(ck)
sc_system_info = sp.control_details(ck)
sp.control_details(ck)
# {'User Account and Authentication (UAA) Server': [{'control_key': 'AC-4', 'standard_key': 'NIST-800-53', 'covered_by': [], 'implementation_status': 'none', 'narrative': [{'text': 'The information system enforces approved authorizations for controlling the flow of information within the system and between interconnected systems based on the 18F Access Control Policy Section 3 -  Information Flow Enforcement which states:\n  - 18F enforces approved authorizations for controlling the flow of information within its information systems and between interconnected systems in accordance with applicable federal laws and 18F policies and procedures.\n  - 18F shall use flow control restrictions to include: keeping export controlled information from being transmitted in the clear to the Internet, blocking outside traffic that claims to be from within the organization and not passing any web requests to the Internet that are not from the internal web proxy.\n  - 18F shall use boundary protection devices (e.g., proxies, gateways, guards, encrypted tunnels, firewalls, and routers) that employ rule sets or establish configuration settings that restrict information system services, provide a packet-filtering capability based on header information, or message-filtering capability based on content (e.g., using key word searches or document characteristics.'}]}]}

# Print control info from standard and also systempl implementation details
print ck
print sc_standard_info.title
print sc_standard_info.description
print yaml.dump(sc_system_info[sc_system_info.keys()[0]])

# Test loading GovCloud OpenControl component yaml directly
component_list = ['AC_Policy','AT_Policy','AU_Policy','CA_Policy','CICloudGov','CM_Policy','CP_Policy','CloudCheckr','ELKStack','IA_Policy','IR_Policy','JumpBox','MA_Policy','MP_Policy','PE_Policy','PL_Policy','PS_Policy','RA_Policy','SA_Policy','SC_Policy','SI_Policy','SecureProxy']
urls = ["https://raw.githubusercontent.com/18F/cg-compliance/master/%s/component.yaml" % comp for comp in component_list]
for compurl in urls:
  sp.system_component_add_from_url(compurl)

pprint.pprint(sp.control_details("AU-1"))


#### OLDER

# load file 1
sp.load_ocfile_from_url(f1)
# load file 1
sp.load_ocfile_from_url(f2)

# loop though what controls are statisfied by second `f2` OpenControl YAML file
# demonstrate combining OpenControl content with ComplianceLib content
for c in sp.ocfiles[f2]['satisfies']: 
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

for c in sp.ocfiles[f2]['satisfies']: 
    print c['control_key']
    cd = compliancelib.NIST800_53(c['control_key'])
    print cd.title

# If we build an index of control_keys, then we can look up control details easily,
# but we have to remember that a control_key can be in more than one component file

cks2 = {}
for kf in sp.ocfiles.keys():
  print kf
  for c in sp.ocfiles[kf]['satisfies']:
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
# sp.ocfiles[cks[sc.id]]['satisfies']
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

class SystemCompliance():
    "initialize OpenControl security controls implementation"
    def __init__(self):
        self.ocfiles = {}
        self.dummy_func()
        # define the dictionaries we will support so we avoid unexpected data
        self.supported_dictionaries = ['components', 'standards', 'certifications', 'assignments', 'roles']
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
      self.system['assignments'] = {}
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
          self.system[dict_type][my_dict['name']] = my_dict
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
        "standards" : self.system['standards'].keys(),
        "certifications" : self.system['certifications'].keys()}
      return scpa

    # Control information
    def control_details(self, cid):
      control_key =  cid
      # if components loaded, look through
      if len(self.system_component_list()) < 1:
        raise Exception ("No controls available. No components have been loaded.")
      else:
        # look through components for control
        control_component_dict = {}
        for component in self.system_component_list():
          component_control_info = [ck for ck in self.system['components'][component]['satisfies'] if ck['control_key'] == control_key]
          if (len(component_control_info)) > 0:
            control_component_dict[component] = component_control_info
      return control_component_dict

      # if cid not in ['AC-3', 'SA-4']:
      #   status = "404"
      #   status_message = "Requested information does not exist"
      #   # {"control_key": ck, "status" : "404", "status_message" : "Requested information does not exist"})
      # cd = { "control_key" : control_key,
      #   "status" : status,
      #   "status_message" : status_message
      #   }
      # return cd
