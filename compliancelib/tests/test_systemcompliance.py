#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
LICENSE

ComplianceLib SystemComplianceTest is a class for testing complianclib.SystemCompliance
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
"""

__author__ = "Greg Elin (gregelin@govready.com)"
__version__ = "$Revision: 0.2.0 $"
__date__ = "$Date: 2016/07/18 07:27:00 $"
__copyright__ = "Copyright (c) 2016 GovReady PBC"
__license__ = "Apache Software License 2.0"

from unittest import TestCase

import compliancelib
import os
import json
import yaml

from compliancelib import SystemCompliance
import sys

if sys.version_info >= (3, 0):
    from urllib.parse import urlparse
    from urllib.request import urlopen
if sys.version_info < (3, 0) and sys.version_info >= (2, 5):
    from urlparse import urlparse
    from urllib2 import urlopen

class SystemComplianceTest(TestCase):
    
    def test(self):
        self.assertTrue(True)

    def test_create_system_dictionary(self):
        "Test system dictionary created"
        sp = SystemCompliance()
        # test empty oc
        self.assertTrue(len(sp.ocfiles) == 0)
        # test necessary dictionaries created
        self.assertTrue(sp.system is not None)
        self.assertTrue(sp.system['components'] is not None)

        # test that empty system object exists
        self.assertTrue(sp.system['name'] == "")

    def test_add_component_from_url(self):
        "Test method 'add_component_from_url'"
        sp = SystemCompliance()
        ocfileurl = 'https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml'
        sp.add_component_from_url(ocfileurl)
        print(sp.components())
        self.assertTrue(sp.components() == ['Audit Policy'])

    def test_components(self):
        "Test system component dictionary"
        sp = SystemCompliance()
        # test necessary dictionaries created
        self.assertTrue(sp.system is not None)

        # test adding in components
        oc_component_file = os.path.join(os.path.dirname(__file__), '../data/UAA_component.yaml')
        print(oc_component_file)
        ocfileurl = "file://%s" % oc_component_file
        test_component_dict = yaml.safe_load(urlopen(ocfileurl))
        sp.system_component_add(test_component_dict['name'], test_component_dict)
        print("system components are %s " % sp.system['components'].keys())
        print(len(sp.system['components']['User Account and Authentication (UAA) Server']['satisfies']))
        self.assertTrue(list(sp.system['components'])[0] == "User Account and Authentication (UAA) Server")
        self.assertTrue(len(sp.system['components']['User Account and Authentication (UAA) Server']['satisfies']) == 26)

        # add second component file and test list of components
        oc_component_file = os.path.join(os.path.dirname(__file__), '../data/AU_policy_component.yaml')
        print(oc_component_file)
        ocfileurl = "file://%s" % oc_component_file
        # this is where we add the component dictionary
        test_component_dict = yaml.safe_load(urlopen(ocfileurl))
        sp.system_component_add(test_component_dict['name'], test_component_dict)

        # test method to get list of system components
        print(sp.components())
        self.assertTrue('Audit Policy' in sp.components())
        self.assertTrue('User Account and Authentication (UAA) Server' in sp.components())
        self.assertFalse('Wrong Name' in sp.components())

    def test_standards(self):
        "Test system standards dictionary"
        sp = SystemCompliance()
        # testing adding a standard
        standard_name = "FRIST-800-53"
        standard_dict = {"name": "FRIST-800-53", "other_key": "some value"}
        sp.add_system_dict('standards', standard_name, standard_dict)
        print(sp.standards())
        self.assertTrue(sp.standards() == ["FRIST-800-53"])
        # To do test for exception case of non-existent dictionary type

    def test_certifications(self):
        "Test system certifications dictionary"
        sp = SystemCompliance()
        # testing adding a certification
        name = "FRed-RAMP-Low"
        my_dict = {"name": "FRed-RAMP-Low", "other_key": "some value"}
        sp.add_system_dict('certifications', name, my_dict)
        self.assertTrue(sp.certifications() == ["FRed-RAMP-Low"])
        # To do test for exception case of non-existent dictionary type 

    def test_roles(self):
        "Test system roles dictionary"
        sp = SystemCompliance()
        # testing adding a role
        name = "SOME VALUE"
        my_dict = {"name": "SOME VALUE", "other_key": "some value"}
        sp.add_system_dict('roles', name, my_dict)
        self.assertTrue(sp.roles() == ["SOME VALUE"])
        # To do test for exception case of non-existent dictionary type

    def test_summary(self):
        "Test outputting basic system compliance profile"
        sp = SystemCompliance()
        # set system name
        sp.system['name'] = "GovReady WordPress Dashboard"
        # add system components
        my_components = ['../data/UAA_component.yaml', '../data/AU_policy_component.yaml']
        [sp.add_component_from_url("file://%s" % os.path.join(os.path.dirname(__file__), ocfileurl)) for ocfileurl in my_components]
        
        # add system standard
        standard_name = "FRIST-800-53"
        standard_dict = {"name": "FRIST-800-53", "other_key": "some value"}
        sp.add_system_dict('standards', standard_name, standard_dict)

        # add system certifications
        name = "FRed-RAMP-Low"
        my_dict = {"name": "FRed-RAMP-Low", "other_key": "some value"}
        sp.add_system_dict('certifications', name, my_dict)

        # Test system compliance profile
        print("System compliance summary %s" % sp.summary())
        print(sp.summary()['components'])
        print("********")
        self.assertTrue(sp.summary()['standards'] == ['FRIST-800-53'])
        self.assertTrue(sp.summary()['certifications'] == ['FRed-RAMP-Low'])
        self.assertTrue('Audit Policy' in sp.summary()['components'])
        self.assertTrue('User Account and Authentication (UAA) Server' in sp.summary()['components'])
        self.assertTrue(sp.summary()['name'] == 'GovReady WordPress Dashboard')

    def test_control(self):
        "Test the control implementation object"
        # instantiate SystemCompliance object and populate to test
        sp = SystemCompliance()
        sp.system['name'] = "GovReady WordPress Dashboard"
        my_components = ['../data/UAA_component.yaml', '../data/AU_policy_component.yaml']
        [sp.add_component_from_url("file://%s" % os.path.join(os.path.dirname(__file__), ocfileurl)) for ocfileurl in my_components]
        standard_name = "FRIST-800-53"
        standard_dict = {"name": "FRIST-800-53", "other_key": "some value"}
        sp.add_system_dict('standards', standard_name, standard_dict)
        name = "FRed-RAMP-Low"
        my_dict = {"name": "FRed-RAMP-Low", "other_key": "some value"}
        sp.add_system_dict('certifications', name, my_dict)

        #
        # System instantiated, let's test displaying control information
        #

        # report when a control is not found
        ck = "AC-200" # no such control
        ci = sp.control(ck)
        print("%s info is %s " % (ck, ci.title))
        print("\n")
        self.assertTrue(ci.id == "AC-200")
        self.assertTrue(ci.title == None)
        self.assertTrue(ci.description == None)
        self.assertTrue(ci.responsible == None)
        self.assertTrue(ci.components_dict == {})
        # TODO Test implementation_status
        # TODO Test implementation_status_details

        ck = "AU-1"
        ci = sp.control(ck)
        print(ci.id)
        print(ci.title)
        print(ci.description)
        print("\nSystem control implmentation details")
        print("-------------------------------------")
        print(ci.components)
        print(ci.implementation_narrative)
        self.assertTrue(ci.id == "AU-1")
        self.assertTrue(ci.title == 'AUDIT AND ACCOUNTABILITY POLICY AND PROCEDURES')
        self.assertTrue(ci.description == """The organization:
a. Develops, documents, and disseminates to [Assignment: organization-defined personnel or roles]:
a.1. An audit and accountability policy that addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
a.2. Procedures to facilitate the implementation of the audit and accountability policy and associated audit and accountability controls; and
b. Reviews and updates the current:
b.1. Audit and accountability policy [Assignment: organization-defined frequency]; and
b.2. Audit and accountability procedures [Assignment: organization-defined frequency].""")
        self.assertTrue(ci.responsible == 'organization')
        self.assertTrue(ci.components == ['Audit Policy'])

        # report when a control is  found
        ck = "AC-4"
        ci = sp.control(ck)
        print(ci.id)
        print(ci.title)
        print(ci.description)
        print("\nSystem control implmentation details")
        print("-------------------------------------")
        print(ci.components)
        print(ci.implementation_narrative)
        self.assertTrue(ci.id == "AC-4")
        self.assertTrue(ci.title == 'INFORMATION FLOW ENFORCEMENT')
        self.assertTrue(ci.description == 'The information system enforces approved authorizations for controlling the flow of information within the system and between interconnected systems based on [Assignment: organization-defined information flow control policies].')
        self.assertTrue(ci.responsible == 'information system')
        self.assertTrue(ci.components == ['User Account and Authentication (UAA) Server'])

        # test control enhancement id
        ck = "AC-2 (1)"
        ci = sp.control(ck)
        print(ci.id)
        print(ci.title)
        print(ci.description)
        print("\nSystem control implmentation details")
        print("-------------------------------------")
        print(ci.components)
        print(ci.implementation_narrative)
        self.assertTrue(ci.id == "AC-2 (1)")
        self.assertTrue(ci.title == 'AUTOMATED SYSTEM ACCOUNT MANAGEMENT')
        self.assertTrue(ci.description == 'The organization employs automated mechanisms to support the management of information system accounts.')
        self.assertTrue(ci.responsible == None)
        self.assertTrue(ci.components == ['User Account and Authentication (UAA) Server'])

    def test_control_ssp_text(self):
        "Test print out text for a control listing in system security plan (assume NIST800-53)"
        print("Need tests written for this method")
        # self.assertTrue(1==2)

    def test_load_system_from_opencontrol_repo(self):
        "Test load system details and control implementation from a repo"
        print("Need tests test written for this method")
        # self.assertTrue(1==2)

if __name__ == "__main__":
    unittest.main()