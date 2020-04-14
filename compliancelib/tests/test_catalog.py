"""
LICENSE

ComplianceLib NIST800_53VizTest is a class for testing complianclib.NIST800_53Viz
Copyright (C) 2020  GovReady PBC.

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

import unittest
# import sys
import os
import json


from compliancelib import Catalogs, Catalog
#from compliancelib import NIST800_53

class CatalogsTest(unittest.TestCase):

    # Setup
    def get_catalog_80053_rev4(self):
        catalogs = Catalogs()
        catalog_file = "NIST_SP-800-53_rev4_catalog.json"
        catalog = catalogs._load_catalog_json(catalog_file)
        return catalog

    def get_catalog_80053_rev5(self):
        catalogs = Catalogs()
        catalog_file = "NIST_SP-800-53_rev5_catalog.json"
        catalog = catalogs._load_catalog_json(catalog_file)
        return catalog

    # Tests
    def test(self):
        self.assertTrue(True)

    def test_catalog_load_catalog_json(self):
        catalog = self.get_catalog_80053_rev4()
        self.assertEqual("uuid-26a2a133-f395-432c-b2ad-77d23a23ca4e",catalog['id'])

    def test_catalog_list(self):
        catalog = self.get_catalog_80053_rev4()


class CatalogTest(unittest.TestCase):

    # Setup
    def get_catalog_80053_rev4(self):
        catalog_file = "NIST_SP-800-53_rev4_catalog.json"
        catalog = Catalog(catalog_file)
        return catalog

    def get_catalog_80053_rev5(self):
        catalog_file = "NIST_SP-800-53_rev5_catalog.json"
        catalog = Catalog(catalog_file)
        return catalog

    # Tests
    def test(self):
        self.assertTrue(True)

    def test_catalog_load_catalog_json(self):
        catalog = self.get_catalog_80053_rev4()
        self.assertEqual("uuid-26a2a133-f395-432c-b2ad-77d23a23ca4e", catalog.catalog_oscal['id'])

    def test_get_groups(self):
        catalog = self.get_catalog_80053_rev4()
        groups = catalog.get_groups()
        # print("groups", len(groups))
        self.assertEqual(len(groups), 18)

    def test_get_primary_control_id_list(self):
        catalog = self.get_catalog_80053_rev4()
        self.assertEqual(len(catalog.primary_control_ids), 18)


