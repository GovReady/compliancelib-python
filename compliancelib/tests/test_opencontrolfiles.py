#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Greg Elin (gregelin@govready.com)"
__version__ = "$Revision: 0.2.0 $"
__date__ = "$Date: 2016/07/23 09:27:00 $"
__copyright__ = "Copyright (c) 2016 GovReady PBC"
__license__ = "Apache Software License 2.0"

from unittest import TestCase

import compliancelib
import os
import json
import yaml
from compliancelib import OpenControlFiles

class OpenControlFilesTest(TestCase):
    
    def test(self):
        self.assertTrue(True)

    def test_load_ocfile(self):
        "Test loading of an OpenControl component YAML file"
        ocfileurl = "https://raw.githubusercontent.com/opencontrol/freedonia-compliance/master/AU_policy/component.yaml"
        ocf = OpenControlFiles()
        # test empty oc
        self.assertTrue(len(ocf.ocfiles) == 0)
        # load an OpenControl file
        ocf.load_ocfile_from_url(ocfileurl)
        print len(ocf.ocfiles)
        print list(ocf.ocfiles.keys())
        #  test length of ocfiles
        self.assertTrue(len(ocf.ocfiles) == 1)
        # self.assertTrue(ocf.list_files() == "https://github.com/pburkholder/freedonia-compliance/blob/master/AU_policy/component.yaml")
        # test not loading same file twice
        ocf.load_ocfile_from_url(ocfileurl)
        self.assertTrue(len(ocf.ocfiles) == 1)
        # load second file
        ocfileurl2 = 'https://raw.githubusercontent.com/opencontrol/cf-compliance/master/UAA/component.yaml'
        ocf.load_ocfile_from_url(ocfileurl2)
        self.assertTrue(len(ocf.ocfiles) == 2)
        print ocf.ocfiles.keys()
        self.assertTrue('https://raw.githubusercontent.com/opencontrol/cf-compliance/master/UAA/component.yaml' in ocf.ocfiles.keys())
        self.assertTrue('https://raw.githubusercontent.com/opencontrol/freedonia-compliance/master/AU_policy/component.yaml' in ocf.ocfiles.keys())
        # test loading if opencontrol file already in ocfiles object
        print ocf.load_ocfile_from_url(ocfileurl)
        print ocf.ocfiles.keys()
        self.assertTrue(ocf.load_ocfile_from_url(ocfileurl)=={'documentation_complete': False, 'references': [{'path': 'https://github.com/opencontrol/freedonia-policies/wiki/Audit-Policy', 'name': 'AU Policy'}], 'satisfies': [{'control_key': 'AU-1', 'standard_key': 'FRIST-800-53', 'covered_by': [], 'implementation_status': 'complete', 'narrative': [{'text': 'This text describes how our organization is meeting the requirements for the\nAudit policy, and also references a more complete description at ./AU_policy/README.md\n\nSince the AU-1 `control` is to document and disseminate a policy on Audit and Accountability, then\nthis narrative suffices to provide that control. A verification step could be something\nthat checks that the referenced policy is no more than 365 days old.\n'}]}, {'control_key': 'AU-2', 'standard_key': 'FRIST-800-53', 'covered_by': [], 'implementation_status': 'none', 'narrative': [{'text': "Application and Server logs are sent to PaperTrail to provide audit\nreduction and report generation capabilites for Freedonia Devops and end users\nof the Freedonia hello_world system.\n\nPaperTrail is a SaaS for aggregation of audit log data across multiple systems and tiers\n\nWith the PaperTrail capability the organizations's operations and development teams\ncan structure and customize audit logs queries to specific app instances, API\ncalls, system metrics, user access, system components, network traffic flow and\nother criteria.\n"}]}], 'schema_version': '3.0.0', 'name': 'Audit Policy'})

    def test_resolve_ocfile_url(self):
        "Test resolution of a opencontrol.yaml url"
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        revision = 'master'
        component_path = ''
        correct_url = ocf.resolve_ocfile_url(repo_ref, revision)
        self.assertTrue( 'https://raw.githubusercontent.com/18F/cg-compliance/master/opencontrol.yaml' == correct_url)

    def test_resolve_component_url(self):
        "Test resolution of a component url"
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        revision = 'master'
        component_path = './CloudCheckr'
        # repo_url, revision, path, yaml_file = 'component.yaml'
        correct_url = ocf.resolve_component_url(repo_ref, revision, component_path)
        self.assertTrue( 'https://raw.githubusercontent.com/18F/cg-compliance/master/./CloudCheckr/component.yaml' == correct_url)

    def test_parse_opencontrolfile(self):
        "Test retrieve and parsing of an opencontrol.yaml file"
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        revision = 'master'
        component_path = ''
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        my_dict = ocf.load_ocfile_from_url(ocfileurl)
        print my_dict.keys()
        print "------"
        print my_dict['components']
        self.assertTrue(len(my_dict.keys()) == 5)
        self.assertTrue('metadata' in my_dict.keys())
        self.assertTrue('dependencies' in my_dict.keys())
        self.assertTrue('components' in my_dict.keys())
        self.assertTrue('name' in my_dict.keys())
        self.assertTrue('schema_version' in my_dict.keys())
        #TODO the following test is brittle
        self.assertTrue(['metadata', 'dependencies', 'name', 'components', 'schema_version'] ==  my_dict.keys())

    def test_list_components_in_repo(self):
        "Test generating a list of components from opencontrol.yaml file"
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        revision = 'master'
        component_path = ''
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        # load opencontrol.yaml file
        components = ocf.list_components_in_repo(ocfileurl)
        self.assertTrue(['./AC_Policy', './AT_Policy', './AU_Policy', './CA_Policy', './CICloudGov', './CM_Policy', './CP_Policy', './CloudCheckr', './ELKStack', './IA_Policy', './IR_Policy', './JumpBox', './MA_Policy', './MP_Policy', './PE_Policy', './PL_Policy', './PS_Policy', './RA_Policy', './SA_Policy', './SC_Policy', './SI_Policy', './SecureProxy'] == components)
        # self.assertTrue( 1 == 2)

    def test_list_components_urls_in_repo(self):
        "Test generating a list of component URL files from opencontrol.yaml file"
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        revision = 'master'
        component_path = ''
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        print "repo_ref 1: %s" % repo_ref
        print "ocfileurl 1: ocfileurl %s" % ocfileurl
        # load opencontrol.yaml file
        components_urls = ocf.list_components_urls_in_repo(ocfileurl)
        # print components_urls
        self.assertTrue(len(components_urls) == 22)
        self.assertTrue('https://raw.githubusercontent.com/18F/cg-compliance/master/./AC_Policy/component.yaml' in components_urls)
        self.assertTrue('https://raw.githubusercontent.com/18F/cg-compliance/master/./ELKStack/component.yaml' in components_urls)
        self.assertTrue('https://raw.githubusercontent.com/18F/cg-compliance/master/./MA_Policy/component.yaml' in components_urls)
        self.assertTrue('https://raw.githubusercontent.com/18F/cg-compliance/master/./CICloudGov/component.yaml' in components_urls)
        # test with other repo
        repo_ref = 'https://github.com/opencontrol/freedonia-compliance'
        revision = 'master'
        component_path = ''
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        print "ocfileurl 2: ocfileurl %s" % ocfileurl
        # load opencontrol.yaml file
        components_urls = ocf.list_components_urls_in_repo(ocfileurl)
        print components_urls
        self.assertTrue(len(components_urls) == 1)
        self.assertTrue(['https://raw.githubusercontent.com/opencontrol/freedonia-compliance/master/./AU_policy/component.yaml'] == components_urls)


if __name__ == "__main__":
    unittest.main()