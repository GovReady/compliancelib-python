from unittest import TestCase

import compliancelib
import sys
import os
import json
import yaml

# sys.path.append(os.path.join('lib'))
# sys.path.append(os.path.join('data'))
from compliancelib import SecControl

class SecControlTest(TestCase):
	
	def test(self):
		self.assertTrue(True)

	def test_id(self):
		id = "AT-3"
		c = SecControl(id)
		self.assertTrue(id == c.id)

	def test_details(self):
		id = "AT-3"
		c = SecControl(id)
		self.assertTrue(c.title == "ROLE-BASED SECURITY TRAINING")

	def test_details_control_enhancement(self):
		id = "AU-3 (1)"
		c = SecControl(id)
		self.assertTrue(c.title == "ADDITIONAL AUDIT INFORMATION")
		self.assertTrue(c.description == "The information system generates audit records containing the following additional information: [Assignment: organization-defined additional, more detailed information].")

	def test_no_existing_control(self):
		id = "XY-3000"
		c = SecControl(id)
		self.assertTrue(c.title == None)
		self.assertTrue(c.description == None)
		self.assertTrue(c.supplemental_guidance == None)
		self.assertTrue(c.responsible == None)
		self.assertTrue(c.details == {})

	def test_details_nonexistent_control(self):
		id = "AX-3"
		c = SecControl(id)
		self.assertTrue(c.title == None)

	def test_supplemental_guidance(self):
		id = "AC-16"
		c = SecControl(id)
		self.assertTrue(c.supplemental_guidance == "Information is represented internally within information systems using abstractions known as data structures. Internal data structures can represent different types of entities, both active and passive. Active entities, also known as subjects, are typically associated with individuals, devices, or processes acting on behalf of individuals. Passive entities, also known as objects, are typically associated with data structures such as records, buffers, tables, files, inter-process pipes, and communications ports. Security attributes, a form of metadata, are abstractions representing the basic properties or characteristics of active and passive entities with respect to safeguarding information. These attributes may be associated with active entities (i.e., subjects) that have the potential to send or receive information, to cause information to flow among objects, or to change the information system state. These attributes may also be associated with passive entities (i.e., objects) that contain or receive information. The association of security attributes to subjects and objects is referred to as binding and is typically inclusive of setting the attribute value and the attribute type. Security attributes when bound to data/information, enables the enforcement of information security policies for access control and information flow control, either through organizational processes or information system functions or mechanisms. The content or assigned values of security attributes can directly affect the ability of individuals to access organizational information.\nOrganizations can define the types of attributes needed for selected information systems to support missions/business functions. There is potentially a wide range of values that can be assigned to any given security attribute. Release markings could include, for example, US only, NATO, or NOFORN (not releasable to foreign nationals). By specifying permitted attribute ranges and values, organizations can ensure that the security attribute values are meaningful and relevant. The term security labeling refers to the association of security attributes with subjects and objects represented by internal data structures within organizational information systems, to enable information system-based enforcement of information security policies. Security labels include, for example, access authorizations, data life cycle protection (i.e., encryption and data expiration), nationality, affiliation as contractor, and classification of information in accordance with legal and compliance requirements. The term security marking refers to the association of security attributes with objects in a human-readable form, to enable organizational process-based enforcement of information security policies. The AC-16 base control represents the requirement for user-based attribute association (marking). The enhancements to AC-16 represent additional requirements including information system-based attribute association (labeling). Types of attributes include, for example, classification level for objects and clearance (access authorization) level for subjects. An example of a value for both of these attribute types is Top Secret.")	

	def test_responsible(self):
		# test "organization"
		id = "AT-3"
		c = SecControl(id)
		self.assertTrue(c.responsible == "organization")

		id = "AU-8"
		c = SecControl(id)
		self.assertTrue(c.responsible == "information system")

		# test "[Withdrawn"
		id = "SA-7"
		c = SecControl("SA-7")
		self.assertTrue(c.responsible == "withdrawn")

	def test_generate_json(self):
		# To do - this test does not work
		id = "AT-3"
		c = SecControl(id)
		c_json = c.get_control_json()
		# print c_json
		self.assertTrue(c_json["id"] == c.id)
		self.assertTrue(c_json["title"] == c.title)
		self.assertTrue(c_json["description"] == c.description)
		self.assertTrue(c_json["responsible"] == c.responsible)
		self.assertTrue(c_json["supplemental_guidance"] == c.supplemental_guidance)

		# test for other (not organization, information system, or [Withdrawn)

	def test_generate_yaml(self):
		# To do - this test does not work
		id = "AT-3"
		c = SecControl(id)
		c_yaml = yaml.load(c.get_control_yaml())
		# print c_yaml
		self.assertTrue(c_yaml["id"] == c.id)
		self.assertTrue(c_yaml["title"] == c.title)
		self.assertTrue(c_yaml["description"] == c.description)
		self.assertTrue(c_yaml["responsible"] == c.responsible)
		self.assertTrue(c_yaml["supplemental_guidance"] == c.supplemental_guidance)

		# test for other (not organization, information system, or [Withdrawn)


if __name__ == "__main__":
	unittest.main()
