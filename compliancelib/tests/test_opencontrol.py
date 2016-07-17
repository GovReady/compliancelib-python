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
        ocfile = "https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml"
        oc = OpenControl()
        # test empty oc
        self.assertTrue(len(oc.ocfiles) == 0)
        # load an OpenControl file
        oc.load_ocfile(ocfile)
        print len(oc.ocfiles)
        print list(oc.ocfiles.keys())
        #  test length of ocfiles
        self.assertTrue(len(oc.ocfiles) == 1)
        # self.assertTrue(oc.list_files() == "https://github.com/pburkholder/freedonia-compliance/blob/master/AU_policy/component.yaml")
        # test not loading same file twice
        oc.load_ocfile(ocfile)
        self.assertTrue(len(oc.ocfiles) == 1)
        # load second file
        ocfile2 = 'https://raw.githubusercontent.com/opencontrol/cf-compliance/master/UAA/component.yaml'
        oc.load_ocfile(ocfile2)
        self.assertTrue(len(oc.ocfiles) == 2)
        self.assertTrue(oc.ocfiles.keys() == ['https://raw.githubusercontent.com/opencontrol/cf-compliance/master/UAA/component.yaml', 'https://raw.githubusercontent.com/pburkholder/freedonia-compliance/master/AU_policy/component.yaml'])


if __name__ == "__main__":
    unittest.main()