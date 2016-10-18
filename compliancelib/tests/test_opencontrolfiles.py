#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
LICENSE

ComplianceLib OpenControlFilesTest is a class for testing complianclib.OpenControlFiles
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
__version__ = "$Revision: 0.4.0 $"
__date__ = "$Date: 2016/10/18 05:30:00 $"
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
        print(len(ocf.ocfiles))
        print(list(ocf.ocfiles.keys()))
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
        print(ocf.ocfiles.keys())
        self.assertTrue('https://raw.githubusercontent.com/opencontrol/cf-compliance/master/UAA/component.yaml' in ocf.ocfiles.keys())
        self.assertTrue('https://raw.githubusercontent.com/opencontrol/freedonia-compliance/master/AU_policy/component.yaml' in ocf.ocfiles.keys())
        # test loading if opencontrol file already in ocfiles object
        print(ocf.load_ocfile_from_url(ocfileurl))
        print(ocf.ocfiles.keys())
        print("ALERT: If this test fails, first check if ocfileurl content has changed!")
        self.assertTrue(ocf.load_ocfile_from_url(ocfileurl)=={'documentation_complete': False, 'references': [{'path': 'https://github.com/opencontrol/freedonia-policies/wiki/Audit-Policy', 'name': 'AU Policy'}], 'satisfies': [{'control_key': 'AU-1', 'standard_key': 'FRIST-800-53', 'covered_by': [], 'implementation_status': 'implemented', 'narrative': [{'text': 'This text describes how our organization is meeting the requirements for the\nAudit policy, and also references a more complete description at ./AU_policy/README.md\n\nSince the AU-1 `control` is to document and disseminate a policy on Audit and Accountability, then\nthis narrative suffices to provide that control. A verification step could be something\nthat checks that the referenced policy is no more than 365 days old.\n'}]}, {'control_key': 'AU-2', 'standard_key': 'FRIST-800-53', 'covered_by': [], 'implementation_status': 'none', 'narrative': [{'text': "Application and Server logs are sent to PaperTrail to provide audit\nreduction and report generation capabilites for Freedonia Devops and end users\nof the Freedonia hello_world system.\n\nPaperTrail is a SaaS for aggregation of audit log data across multiple systems and tiers\n\nWith the PaperTrail capability the organizations's operations and development teams\ncan structure and customize audit logs queries to specific app instances, API\ncalls, system metrics, user access, system components, network traffic flow and\nother criteria.\n"}]}], 'schema_version': '3.0.0', 'name': 'Audit Policy'})

    def test_resolve_ocfile_url_github(self):
        "Test resolution of a opencontrol.yaml url"
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        revision = 'master'
        component_path = ''
        correct_url = ocf.resolve_ocfile_url(repo_ref, revision)
        self.assertTrue( 'https://raw.githubusercontent.com/18F/cg-compliance/master/opencontrol.yaml' == correct_url)

    def test_resolve_ocfile_url_localfile(self):
        "Test resolution of a opencontrol.yaml url that is a localfile"
        ocf = OpenControlFiles()
        # construct absolute file path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        repo_ref = "file://{}/{}".format(dir_path, "test_data/repo1")
        print("dir_path is {}".format(dir_path))
        print("repo_ref is {}".format(repo_ref))
        revision = 'master'
        component_path = ''
        correct_url = ocf.resolve_ocfile_url(repo_ref, revision)
        self.assertTrue( "{}/{}".format(repo_ref,'opencontrol.yaml') == correct_url)

    def test_resolve_item_url_github(self):
        "Test resolution of a component url"
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        revision = 'master'
        item_type = "components"
        component_path = './CloudCheckr'
        # repo_url, revision, path, yaml_file = 'component.yaml'
        correct_url = ocf.resolve_item_url(repo_ref, revision, component_path, item_type)
        self.assertTrue( 'https://raw.githubusercontent.com/18F/cg-compliance/master/./CloudCheckr/component.yaml' == correct_url)

    def test_resolve_item_url_localfile(self):
        "Test resolution of a component url that is a localfile"
        ocf = OpenControlFiles()
        # construct absolute file path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        repo_ref = "file://{}/{}".format(dir_path, "test_data/repo1")
        print("dir_path is {}".format(dir_path))
        print("repo_ref is {}".format(repo_ref))
        revision = 'master'
        component_path = './AU_policy'
        item_type = "components"
        resolved_url = ocf.resolve_item_url(repo_ref, revision, component_path, item_type)
        expected_url = "{}/{}/{}".format(repo_ref, component_path, 'component.yaml')
        print("expected_url is {}".format(expected_url))
        print("resolved_url is {}".format(resolved_url))
        self.assertTrue(expected_url == resolved_url)

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
        print(my_dict.keys())
        print("------")
        print(my_dict['components'])
        self.assertTrue(len(list(my_dict)) == 5)
        self.assertTrue('metadata' in list(my_dict))
        self.assertTrue('dependencies' in list(my_dict))
        self.assertTrue('components' in list(my_dict))
        self.assertTrue('name' in list(my_dict))
        self.assertTrue('schema_version' in list(my_dict))

    def test_list_items_in_repo(self):
        "Test generating a list of components from opencontrol.yaml file"
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        revision = 'master'
        component_path = ''
        item_type = "components"
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        # load opencontrol.yaml file
        components = ocf.list_items_in_repo(ocfileurl, item_type)
        self.assertTrue(['./AC_Policy', './AT_Policy', './AU_Policy', './CA_Policy', './CICloudGov', './CM_Policy', './CP_Policy', './CloudCheckr', './ELKStack', './IA_Policy', './IR_Policy', './JumpBox', './MA_Policy', './MP_Policy', './PE_Policy', './PL_Policy', './PS_Policy', './RA_Policy', './SA_Policy', './SC_Policy', './SI_Policy', './SecureProxy'] == components)
        # self.assertTrue( 1 == 2)

    def test_list_items_in_repo_no_key(self):
        "Test graceful failure of a list of items for a item_type that is not listed in opencontrol.yaml file"
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        revision = 'master'
        component_path = ''
        item_type = "standards"
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        # load opencontrol.yaml file
        items = ocf.list_items_in_repo(ocfileurl, item_type)
        self.assertTrue([] == items)
        # self.assertTrue( 1 == 2)

    def test_list_items_urls_in_repo(self):
        "Test generating a list of items (components, standards, certifications, etc) URL files from opencontrol.yaml file"
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        revision = 'master'
        component_path = ''
        # test for graceful handling of non-existent item_type
        item_type = "standardsx"
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        print("repo_ref 1: %s" % repo_ref)
        print("ocfileurl 1: ocfileurl %s" % ocfileurl)
        # load opencontrol.yaml file
        components_urls = ocf.list_items_urls_in_repo(ocfileurl, item_type)
        self.assertTrue(len(components_urls) == 0)

        # test for existing item_type "components"
        item_type = "components"
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        print("repo_ref 1: %s" % repo_ref)
        print("ocfileurl 1: ocfileurl %s" % ocfileurl)
        # load opencontrol.yaml file
        components_urls = ocf.list_items_urls_in_repo(ocfileurl, item_type)
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
        item_type = "components"
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        print("ocfileurl 2: ocfileurl %s" % ocfileurl)
        # load opencontrol.yaml file
        components_urls = ocf.list_items_urls_in_repo(ocfileurl, item_type)
        print(components_urls)
        self.assertTrue(len(components_urls) == 1)
        self.assertTrue(['https://raw.githubusercontent.com/opencontrol/freedonia-compliance/master/./AU_policy/component.yaml'] == components_urls)

        # test for components with repo on localfile system
        print("\n******* test repo on localfile system ****")
        # construct absolute file path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        repo_ref = "file://{}/{}".format(dir_path, "test_data/repo1")
        # resolve the `opencontrol.yaml` file
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        # print debug info
        print("dir_path is {}".format(dir_path))
        print("repo_ref is {}".format(repo_ref))
        print("ocfileurl 3: ocfileurl %s" % ocfileurl)
        revision = 'master'
        item_type = "components"
        components_urls = ocf.list_items_urls_in_repo(ocfileurl, item_type)
        # components_urls = ["a", "b"]
        print("component_urls equal {}".format(components_urls))
        expected_url = "file://{}/{}".format(dir_path, "test_data/repo1/./AU_policy/component.yaml")
        print("expected_url is {}".format(expected_url))
        self.assertTrue([expected_url] == components_urls)

        # test for standards with repo on localfile system
        # construct absolute file path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        repo_ref = "file://{}/{}".format(dir_path, "test_data/repo2")
        # resolve the `opencontrol.yaml` file
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        # print debug info
        print("dir_path is {}".format(dir_path))
        print("repo_ref is {}".format(repo_ref))
        print("ocfileurl 4: ocfileurl %s" % ocfileurl)
        revision = 'master'
        item_type = "standards"
        items_urls = ocf.list_items_urls_in_repo(ocfileurl, item_type)
        print("items_urls equal {}".format(items_urls))
        expected_url = "file://{}/{}".format(dir_path, "test_data/repo2/./standards/FRIST-800-53.yaml")
        print("expected_url is {}".format(expected_url))
        self.assertTrue([expected_url] == items_urls)

        # test for certifications with repo on localfile system
        # construct absolute file path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        repo_ref = "file://{}/{}".format(dir_path, "test_data/repo2")
        # resolve the `opencontrol.yaml` file
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        # print debug info
        print("dir_path is {}".format(dir_path))
        print("repo_ref is {}".format(repo_ref))
        print("ocfileurl 4: ocfileurl %s" % ocfileurl)
        revision = 'master'
        item_type = "certifications"
        items_urls = ocf.list_items_urls_in_repo(ocfileurl, item_type)
        print("************\n items_urls equal {}".format(items_urls))
        expected_urls = ["file://{}/{}".format(dir_path, "test_data/repo2/./certifications/FredRAMP-low.yaml"), "file://{}/{}".format(dir_path, "test_data/repo2/./certifications/LATO.yaml")]
        print("expected_urls is {}".format(expected_urls))
        self.assertTrue("file://{}/{}".format(dir_path, "test_data/repo2/./certifications/FredRAMP-low.yaml") in items_urls)
        self.assertTrue("file://{}/{}".format(dir_path, "test_data/repo2/./certifications/LATO.yaml") in items_urls)

    def test_list_standards_in_repo(self):
        "Test listing of standards from opencontrol.yaml file"
        ocf = OpenControlFiles()
        # test with repo on localfile system with local and remote certifications references
        print("\n******* test repo on localfile system ****")
        revision = 'master'
        item_type = "standards"
        # construct absolute file path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        repo_ref = "file://{}/{}".format(dir_path, "test_data/repo2")
        # resolve the `opencontrol.yaml` file
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        items = ocf.list_items_in_repo(ocfileurl, item_type)
        print("ocf.list_items_in_repo: ", items)
        self.assertTrue(['./standards/FRIST-800-53.yaml'] == items)

    def test_list_certifications_in_repo(self):
        "Test generating a list of certifications from opencontrol.yaml file"
        ocf = OpenControlFiles()
        # test with repo on localfile system with local and remote certifications references
        print("\n******* test repo on localfile system ****")
        revision = 'master'
        item_type = "certifications"
        # construct absolute file path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        repo_ref = "file://{}/{}".format(dir_path, "test_data/repo2")
        # resolve the `opencontrol.yaml` file
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        items = ocf.list_items_in_repo(ocfileurl, item_type)
        print("ocf.list_items_in_repo: ", items)
        self.assertTrue('./certifications/FredRAMP-low.yaml' in items)
        self.assertTrue('./certifications/LATO.yaml' in items)

    def test_list_dependency_items_in_repo(self):
        "Test generating a list of items from opencontrol.yaml file dependencies section"
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        revision = 'master'
        component_path = ''
        item_type = "systems"
        ocfileurl = ocf.resolve_ocfile_url(repo_ref, revision)
        # load opencontrol.yaml file
        items = ocf.list_dependency_items_in_repo(ocfileurl, item_type)
        print("test_list_dependency_items_in_repo 'standards' are: ", items)
        self.assertTrue({'revision': 'master', 'url': 'https://github.com/opencontrol/cf-compliance'} in items)
        self.assertTrue({'revision': 'master', 'url': 'https://github.com/opencontrol/aws-compliance'} in items)
        # test certifications
        item_type = "certifications"
        items = ocf.list_dependency_items_in_repo(ocfileurl, item_type)
        print("test_list_dependency_items_in_repo 'certfications' are: ", items)
        self.assertTrue({'revision': 'master', 'url': 'https://github.com/opencontrol/FedRAMP-Certifications'} in items)
        # test non-existent type
        item_type = "non-existent-type"
        items = ocf.list_dependency_items_in_repo(ocfileurl, item_type)
        print("test_list_dependency_items_in_repo 'non-existent-type' are: ", items)
        self.assertTrue([] == items)

if __name__ == "__main__":
    unittest.main()