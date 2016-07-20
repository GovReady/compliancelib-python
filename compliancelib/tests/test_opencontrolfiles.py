#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Greg Elin (gregelin@govready.com)"
__version__ = "$Revision: 0.1.0 $"
__date__ = "$Date: 2016/07/20 07:27:00 $"
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
        ocfileurl = "https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml"
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
        self.assertTrue(ocf.ocfiles.keys() == ['https://raw.githubusercontent.com/opencontrol/cf-compliance/master/UAA/component.yaml', 'https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml'])

    def test_resolve_component_url(self):
        "Test resolution of a component url"
        ocf = OpenControlFiles()
        repo_ref = 'https://github.com/18F/cg-compliance'
        revision = 'master'
        component_path = './CloudCheckr'
        # repo_url, revision, path, yaml_file = 'component.yaml'
        correct_url = ocf.resolve_component_url(repo_ref, revision, component_path)
        self.assertTrue( 'https://raw.githubusercontent.com/18F/cg-compliance/master/./CloudCheckr/component.yaml' == correct_url)


if __name__ == "__main__":
    unittest.main()