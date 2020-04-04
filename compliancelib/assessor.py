#!/usr/bin/python
"""Class for Assessor

Instantiate class with System Description

Methods provide information regarding the operation of the system assessed against
a compliance framework.

This program is part of research for Homeland Open Security Technologies to better
understand how to map security controls to continuous monitoring.

Visit [tbd] for the latest version.

LICENSE

ComplianceLib Assessor is a class for providing information regarding the operation
of a system assessed against a compliance framework.

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

Usage
-----

import sys, yaml, pprint

import compliancelib

# instantiate an Assessor object without a system abstract
a = compliancelib.Assessor()

# simplest system abstract
system_abstract = { 
    "protocol": "system_abstract", 
    "name": "Hello World System", 
    "people":   [{ "role": "operator", "description": "The system requires a person assigned the role of 'operator' to periodically execute the script." }], 
    "processes":[{ "role": "execute",  "description": "The system requires a proceedure 'execute' that runs the script."}], 
    "tools":    [{ "role": "script",   "description": "The system requires tool of type 'script' that when executed by the operator prints "Hello, World!" }]
    }

a = compliancelib.Assessor(system_abstract)
a.system_abstract

# simple system abstract with details

system_abstract = { 
    "protocol": "system_abstract", 
    "name": "Hello World System", 
    "people":   [{ "role": "operator"
    "protocol": "system_abstract", 
    "name": "Hello World System", 
    "people":   [{ "role": "operator", "description": "The system requires one or more persons assigned the role of 'operator' to periodically execute the script." }, 
                 { "role": "developer" , "description": "The system requires one or more persons assigned the role of 'developer' to periodically modify and test the script." }
                ], 
    "processes":[{ "role": "execute" "description": "The system requires a proceedure 'execute' that runs the script."}, 
                 { "role": "test"}, 
                 { "role": "develop" }, 
                 { "role": "deploy" }, 
                 { "role": "onboard people" }, 
                 { "role": "offboard people" }], 
    "tools":    [{ "role": "script" }, 
                 { "role": "programming language" }],
    }

a = compliancelib.Assessor(system_abstract)
a.system_abstract["people"]
a.system_abstract["processes"]
a.system_abstract["tools"]

a.list_people_roles()
a.list_processes_roles()
a.list_tools_roles()



"""

__author__ = "Greg Elin (gregelin@govready.com)"
__version__ = "$Revision: 0.1.0 $"
__date__ = "$Date: 2017/05/05 5:34:00 $"
__copyright__ = "Copyright (c) 2017 GovReady PBC"
__license__ = "GNU General Public License v3 (GPLv3)"

import os
import json
import yaml
import re

class Assessor(object):
    "Assessor the operation of a (IT) System"
    def __init__(self, system_abstract=None):
        self.system_abstract = system_abstract

    def list_people_roles(self):
        if self.system_abstract is None:
            return None
        elif "people" in self.system_abstract and len(self.system_abstract["people"]) > 0:
            return [item["role"] for item in self.system_abstract["people"]]
        else:
            return None

    def list_processes_roles(self):
        if self.system_abstract is None:
            return None
        elif "processes" in self.system_abstract and len(self.system_abstract["processes"]) > 0:
            return [item["role"] for item in self.system_abstract["processes"]]
        else:
            return None

    def list_tools_roles(self):
        if self.system_abstract is None:
            return None
        elif "tools" in self.system_abstract and len(self.system_abstract["tools"]) > 0:
            return [item["role"] for item in self.system_abstract["tools"]]
        else:
            return None
