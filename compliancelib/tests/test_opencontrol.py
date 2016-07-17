#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest import TestCase

import compliancelib
import os
import json
import yaml

from compliancelib import OpenControl

class OpenControlTest(TestCase):
    
    def test(self):
        self.assertTrue(True)

    def test_dummy_func(self):
        oc = OpenControl()
        self.assertTrue(oc.dummy_func() == 3)

    def test_load_ocfile(self):
        "Test loading of an OpenControl component YAML file"
        ocfileurl = "https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml"
        oc = OpenControl()
        # test empty oc
        self.assertTrue(len(oc.ocfiles) == 0)
        # load an OpenControl file
        oc.load_ocfile_from_url(ocfileurl)
        print len(oc.ocfiles)
        print list(oc.ocfiles.keys())
        #  test length of ocfiles
        self.assertTrue(len(oc.ocfiles) == 1)
        # self.assertTrue(oc.list_files() == "https://github.com/pburkholder/freedonia-compliance/blob/master/AU_policy/component.yaml")
        # test not loading same file twice
        oc.load_ocfile_from_url(ocfileurl)
        self.assertTrue(len(oc.ocfiles) == 1)
        # load second file
        ocfileurl2 = 'https://raw.githubusercontent.com/opencontrol/cf-compliance/master/UAA/component.yaml'
        oc.load_ocfile_from_url(ocfileurl2)
        self.assertTrue(len(oc.ocfiles) == 2)
        self.assertTrue(oc.ocfiles.keys() == ['https://raw.githubusercontent.com/opencontrol/cf-compliance/master/UAA/component.yaml', 'https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml'])

    def test_system_dictionary_created(self):
        "Test system dictionary created"
        oc = OpenControl()
        # test empty oc
        self.assertTrue(len(oc.ocfiles) == 0)
        # test necessary dictionaries created
        self.assertTrue(oc.system is not None)
        self.assertTrue(oc.system['components'] is not None)

        # test that empty system object exists
        self.assertTrue(oc.system['name'] == "Test System")

    def test_system_component_add_from_url(self):
        "Test method 'system_component_add_from_url'"
        oc = OpenControl()
        ocfileurl = 'https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml'
        oc.system_component_add_from_url(ocfileurl)
        print oc.system_component_list()
        self.assertTrue(oc.system_component_list() == ['Audit Policy'])

    def test_system_components_info(self):
        "Test system component dictionary"
        oc = OpenControl()
        # test necessary dictionaries created
        self.assertTrue(oc.system is not None)

        # test adding in components
        oc_component_file = os.path.join(os.path.dirname(__file__), '../data/UAA_component.yaml')
        print oc_component_file
        ocfileurl = "file://%s" % oc_component_file
        oc.load_ocfile_from_url(ocfileurl)

        test_component_dict = oc.ocfiles[ocfileurl]
        oc.system_component_add(test_component_dict['name'], test_component_dict)
        print "system components are %s " % oc.system['components'].keys()
        print len(oc.system['components']['User Account and Authentication (UAA) Server']['satisfies'])
        self.assertTrue(oc.system['components'].keys()[0] == "User Account and Authentication (UAA) Server")
        self.assertTrue(len(oc.system['components']['User Account and Authentication (UAA) Server']['satisfies']) == 26)

        # add second component file and test list of components
        oc_component_file = os.path.join(os.path.dirname(__file__), '../data/AU_policy_component.yaml')
        print oc_component_file
        ocfileurl = "file://%s" % oc_component_file
        oc.load_ocfile_from_url(ocfileurl)
        # this is where we add the component dictionary
        oc.system_component_add(oc.ocfiles[ocfileurl]['name'], oc.ocfiles[ocfileurl])

        # test method to get list of system components
        print oc.system_component_list()
        self.assertTrue(oc.system_component_list() == ['Audit Policy', 'User Account and Authentication (UAA) Server'])
        self.assertFalse(oc.system_component_list() == ['User Account and Authentication (UAA) Server', 'Wrong Name'])
        # self.assertTrue(0==1)

    def test_system_standards_info(self):
        "Test system standards dictionary"
        oc = OpenControl()
        # testing adding a standard
        standard_name = "FRIST-800-53"
        standard_dict = {"name": "FRIST-800-53", "other_key": "some value"}
        oc.system_dict_add('standards', standard_name, standard_dict)
        self.assertTrue(oc.system_standard_list() == ["FRIST-800-53"])
        # To do test for exception case of non-existent dictionary type

    def test_system_certifications_info(self):
        "Test system certifications dictionary"
        oc = OpenControl()
        # testing adding a certification
        name = "FRed-RAMP-Low"
        my_dict = {"name": "FRed-RAMP-Low", "other_key": "some value"}
        oc.system_dict_add('certifications', name, my_dict)
        self.assertTrue(oc.system_certification_list() == ["FRed-RAMP-Low"])
        # To do test for exception case of non-existent dictionary type 

    def test_system_roles_info(self):
        "Test system roles dictionary"
        oc = OpenControl()
        # testing adding a role
        name = "SOME VALUE"
        my_dict = {"name": "SOME VALUE", "other_key": "some value"}
        oc.system_dict_add('roles', name, my_dict)
        self.assertTrue(oc.system_role_list() == ["SOME VALUE"])
        # To do test for exception case of non-existent dictionary type

    def test_system_compliance_profile_abstract(self):
        "Test outputting basic system compliance profile"
        oc = OpenControl()
        # set system name
        oc.system['name'] = "GovReady WordPress Dashboard"
        # add system components
        my_components = ['../data/UAA_component.yaml', '../data/AU_policy_component.yaml']
        [oc.system_component_add_from_url("file://%s" % os.path.join(os.path.dirname(__file__), ocfileurl)) for ocfileurl in my_components]
        
        # add system standard
        standard_name = "FRIST-800-53"
        standard_dict = {"name": "FRIST-800-53", "other_key": "some value"}
        oc.system_dict_add('standards', standard_name, standard_dict)

        # add system certifications
        name = "FRed-RAMP-Low"
        my_dict = {"name": "FRed-RAMP-Low", "other_key": "some value"}
        oc.system_dict_add('certifications', name, my_dict)

        # Test system compliance profile
        print "System compliance profile abstract is %s" % oc.system_compliance_profile_abstract()
        self.assertTrue(oc.system_compliance_profile_abstract() == "something")


if __name__ == "__main__":
    unittest.main()