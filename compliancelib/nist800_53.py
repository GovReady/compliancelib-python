#!/usr/bin/python
"""Class for 800-53 Security Controls

Instantiate class with Security Control ID (e.g., AT-2, CM-3).

Methods provide information about the Security Control.


This program is part of research for Homeland Open Security Technologies to better
understand how to map security controls to continuous monitoring.

Visit [tbd] for the latest version.
"""

__author__ = "Greg Elin (gregelin@govready.com)"
__version__ = "$Revision: 0.7.3 $"
__date__ = "$Date: 2015/12/12 19:50:00 $"
__copyright__ = "Copyright (c) 2015 GovReady PBC"
__license__ = "Apache Software License 2.0"

import os
import json
import yaml
import re
import defusedxml.ElementTree as ET


class NIST800_53(object):
    "represent 800-53 security controls"
    def __init__(self, id):
        self.xmlfile = os.path.join(os.path.dirname(__file__), 'data/800-53-controls.xml')
        self.id = id
        if "(" in self.id:
            self._load_control_enhancement_from_xml()
        else:
            self._load_control_from_xml()
        # split description
        self.set_description_sections()
        self._get_control_json_dict()

    def _load_control_from_xml(self):
        "load control detail from 800-53 xml using a pure python process"
        tree = ET.parse(self.xmlfile)
        root = tree.getroot()
        # handle name spaces thusly:
        # namespace:tag => {namespace_uri}tag
        # example: controls:control => {http://scap.nist.gov/schema/sp800-53/feed/2.0}control
        # find first control where number tag value equals id
        sc = root.find("./{http://scap.nist.gov/schema/sp800-53/feed/2.0}control/[{http://scap.nist.gov/schema/sp800-53/2.0}number='%s']" % self.id)
        if sc is not None:
            self.family = sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}family').text.strip()
            self.number = sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}number').text.strip()
            self.title = sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}title').text.strip()
            # test if control withdrawn
            if (sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}withdrawn') is not None):
                # control withdrawn
                self.description = self.control_enhancements = self.supplemental_guidance = None
                self.related_controls = self.priority = None
                self.responsible = 'withdrawn'
                return True
            if (sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}priority') is not None):
                self.priority = sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}priority').text.strip()
            else:
                self.priority = None
            self.description = ''.join(sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}statement').itertext())
            self.description = re.sub(r'[ ]{2,}','',re.sub(r'^[ ]', '',re.sub(r'\n','',re.sub(r'[ ]{2,}',' ',self.description))))
            self.description = self.description.replace(self.id, '\n').strip()
            if (sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}control-enhancements')) is not None:
                self.control_enhancements = ''.join(sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}control-enhancements').itertext())
                self.control_enhancements = re.sub(r'[ ]{2,}','',re.sub(r'^[ ]', '',re.sub(r'[\n ]{2,}','\n',re.sub(r'[ ]{2,}',' ',self.control_enhancements))))
                # self.control_enhancements = self.control_enhancements.replace(self.id, '\n')
            else:
                self.control_enhancements = None
            self.sg = sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}supplemental-guidance')
            self.supplemental_guidance = self.sg.find('{http://scap.nist.gov/schema/sp800-53/2.0}description').text.strip()
            related_controls = []
            for related in self.sg.findall('{http://scap.nist.gov/schema/sp800-53/2.0}related'):
                related_controls.append(related.text.strip())
            self.related_controls = ','.join(related_controls)
            self.responsible = self._get_responsible()
        else:
            self.details = json.loads('{"id": null, "error": "Failed to get security control information from 800-53 xml"}')
            self.title = self.description = self.supplemental_guidance = self.control_enhancements = self.responsible = None
            self.details = {}

    def _load_control_enhancement_from_xml(self):
        "load control enhancement from 800-53 xml using a pure python process"
        tree = ET.parse(self.xmlfile)
        root = tree.getroot()
        # handle name spaces thusly:
        # namespace:tag => {namespace_uri}tag
        # example: controls:control => {http://scap.nist.gov/schema/sp800-53/feed/2.0}control
        # find first control where number tag value equals id
        # sc = root.find("./{http://scap.nist.gov/schema/sp800-53/feed/2.0}control/[{http://scap.nist.gov/schema/sp800-53/2.0}number='%s']" % self.id)
        sc = root.find("./{http://scap.nist.gov/schema/sp800-53/feed/2.0}control/{http://scap.nist.gov/schema/sp800-53/2.0}control-enhancements/{http://scap.nist.gov/schema/sp800-53/2.0}control-enhancement/[{http://scap.nist.gov/schema/sp800-53/2.0}number='%s']" % self.id)
        if sc is not None:
            # self.family = sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}family').text
            self.number = sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}number').text.strip()
            self.title = sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}title').text.strip()
            # self.priority = sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}priority').text
            self.description = ''.join(sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}statement').itertext())
            self.description = re.sub(r'[ ]{2,}','',re.sub(r'^[ ]', '',re.sub(r'\n','',re.sub(r'[ ]{2,}',' ',self.description))))
            self.description = self.description.replace(self.id, '\n').strip()
            self.control_enhancements = None
            self.sg = sc.find('{http://scap.nist.gov/schema/sp800-53/2.0}supplemental-guidance')
            self.supplemental_guidance = self.sg.find('{http://scap.nist.gov/schema/sp800-53/2.0}description').text.strip()
            related_controls = []
            # findall("{http://scap.nist.gov/schema/sp800-53/2.0}supplemental-guidance/{http://scap.nist.gov/schema/sp800-53/2.0}related")
            for related in self.sg.findall('{http://scap.nist.gov/schema/sp800-53/2.0}related'):
                related_controls.append(related.text.strip())
            self.related_controls = ','.join(related_controls)
            self.responsible = None
        else:
            self.details = json.loads('{"id": null, "error": "Failed to get security control information from 800-53 xml"}')
            self.title = self.description = self.supplemental_guidance = self.control_enhancements = self.responsible = None
            self.details = {}

    def _get_responsible(self):
        "determine responsibility"
        m = re.match(r'The organization|The information system|\[Withdrawn', self.description)
        if m:
            return {
                'The organization': 'organization',
                'The information system': 'information system',
                '[Withdrawn': 'withdrawn'
            }[m.group(0)]
        else:
            return "other"

    def format(self, format):
        if (format.lower() == "json"):
            return self._get_control_json()
        if (format.lower() == "yaml"):
            return self._get_control_yaml()
        if (format.lower() == "control-masonry" or format.lower() == "control_masonry"):
            return self._get_control_control_masonry()
        # control format is not defined
        return False

    def _get_control_json_dict(self):
        "produce json dict version of control detail"
        self.json_dict = {}
        self.json_dict['id'] = self.id
        self.json_dict['title'] = self.title
        self.json_dict['description'] = self.description
        self.json_dict['description_intro'] = self.description_intro
        self.json_dict['description_sections'] = self.description_sections
        self.json_dict['responsible'] = self.responsible
        self.json_dict['supplemental_guidance'] = self.supplemental_guidance
        return self.json_dict
        # To Do: needs test

    def _get_control_json(self):
        "produce json version of control detail"
        return json.dumps(self.json_dict)

    def _get_control_yaml(self):
        "produce yaml version of control detail"
        return yaml.safe_dump(self.json_dict, allow_unicode=True, default_flow_style=False, line_break="\n",
            indent=4, explicit_start=False, explicit_end=False,)

    def _get_control_control_masonry(self):
        "produce control masonry yaml version of control detail"
        # get json version
        c = self._get_control_json_dict()
        # replace ":" with "&colon;"
        description_sections = []
        for section in self.description_sections:
            description_sections.append(section.replace(":", "&colon;"))
        c['description_sections'] = description_sections
        c['description'] = self.description.replace(":", "&colon;").replace("\n", " ")
        c['description_intro'] = self.description_intro.replace(":", "&colon;")
        # add 'name' key
        c['name'] = self.title
        # remove unnecessary keys
        c.pop("title", None)
        # c.pop("id", None)
        c.pop("responsible", None)
        c.pop("supplemental_guidance", None)
        return yaml.safe_dump(c, allow_unicode=True, default_flow_style=False, line_break="\n",
            indent=4, explicit_start=False, explicit_end=False,)

    # utility functions
    def set_description_sections(self):
        """ splits a control description by lettered sub-sections """
        if self.description is None:
            self.description_intro = self.description_sections = None
            return True
        # temporarily merge sub-sectionsof sub-sections into sub-section, e.g., '\n\tAC-2h.1.'
        tmp_description = re.sub(r"\n\t[A-Z][A-Z]-[0-9]+[a-z]\.([0-9]+)\.", r" (\1)", self.description)
        # split subsections
        sections = re.compile("\n").split(tmp_description)
        self.description_intro = sections.pop(0)
        self.description_sections = sections
        return True

    def replace_line_breaks(self, text, break_src="\n", break_trg="<br />"):
        """ replace one type of line break with another in text block """
        if text is None:
            return ""
        if break_src in text:
            return break_trg.join(text.split(break_src))
        else:
            return text
