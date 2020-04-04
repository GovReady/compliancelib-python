"""
LICENSE

ComplianceLib NIST800_53Test is a class for testing complianclib.NIST800_53
Copyright (C) 2017 GovReady PBC.

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
__version__ = "$Revision: 0.0.1 $"
__date__ = "$Date: 2017/05/05 5:24:00 $"
__copyright__ = "Copyright (c) 2017 GovReady PBC"
__license__ = "GNU General Public License v3 (GPLv3)"

from unittest import TestCase

import compliancelib
# import sys
import os
import json
import yaml

# sys.path.append(os.path.join('lib'))
# sys.path.append(os.path.join('data'))
from compliancelib import Assessor

class AssessorTest(TestCase):
    
    def test(self):
        self.assertTrue(True)

    def test_system_abstract_none(self):
        "Test Assessor instantiated without a system"
        a = Assessor()
        self.assertTrue(a.system_abstract is None)

