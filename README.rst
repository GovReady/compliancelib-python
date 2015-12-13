compliancelib
=============
Machine readable cybersecurity compliance standards library for Python, starting with FISMA and NIST Risk Management Framework

Source code: https://github.com/govready/compliancelib-python

(For more history, see prototype 800-53-Control-Server (https://github.com/govready/800-53-server))

Goal
----
Create a python class that generates basic information about a FISMA 800-53 security control including:
- [x] Full name of control
- [x] Who has responsibility for control (e.g., organization or information system)

Warning
-------
This is early code. There may be errors!

Requirements
------------
- Python 2.7 or 3.4+
- PyYAML - to generate YAML
- graphviz
- defusedxml

Installation
------------
Compliancelib can be installed with Python pip::

	pip install compliancelib

To install Python pip:

- https://pip.pypa.io/en/stable/installing/
- http://sharadchhetri.com/2014/05/30/install-pip-centos-rhel-ubuntu-debian/


Compliancelib can beinstalled with Python Easy Install::

	easy_install compliancelib

Usage
-----

To use, simply do in python shell::

	Python 2.7.10 (default, Jul 14 2015, 19:46:27) 
	[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.39)] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import compliancelib
	>>> c=compliancelib.NIST800_53("AT-3")
	>>> c.id
	'AT-3'
	>>> c.number
	'AT-3'
	>>> c.title
	'ROLE-BASED SECURITY TRAINING'
	>>> c.family
	'AWARENESS AND TRAINING'
	>>> c.description
	'The organization provides role-based security training to personnel with assigned security roles and 
	responsibilities:\na. Before authorizing access to the information system or performing assigned 
	duties;\nb. When required by information system changes; and\nc. [Assignment: organization-defined 
	frequency] thereafter.'
	>>> c.responsible
	'organization'
	>>> c.supplemental_guidance
	'Organizations determine the appropriate content of security training based on the assigned roles and 
	responsibilities of individuals and the specific security requirements of organizations and the information 
	systems to which personnel have authorized access. In addition, organizations provide enterprise architects,
	information system developers, software developers, acquisition/procurement officials, information system 
	managers, system/network administrators, personnel conducting configuration management and auditing 
	activities, personnel performing independent verification and validation activities, security control 
	assessors, and other personnel having access to system-level software, adequate security-related technical 
	training specifically tailored for their assigned duties. Comprehensive role-based training addresses 
	management, operational, and technical roles and responsibilities covering physical, personnel, and 
	technical safeguards and countermeasures. Such training can include for example, policies, procedures, 
	tools, and artifacts for the organizational security roles defined. Organizations also provide the training 
	necessary for individuals to carry out their responsibilities related to operations and supply chain 
	security within the context of organizational information security programs. Role-based security training 
	also applies to contractors providing services to federal agencies.'
	>>> c.control_enhancements
	'\nAT-3 (1)\nENVIRONMENTAL CONTROLS\nThe organization provides [Assignment: organization-defined personnel or
	roles] with initial and [Assignment: organization-defined frequency] training in the employment and 
	operation of environmental controls.\nEnvironmental controls include, for example, fire suppression and 
	detection devices/systems, sprinkler systems, handheld fire extinguishers, fixed fire hoses, smoke 
	detectors, temperature/humidity, HVAC, and power within the facility. Organizations identify personnel with 
	specific roles and responsibilities associated with environmental controls requiring specialized training.
	\nPE-1\nPE-13\nPE-14\nPE-15\nAT-3 (2)\nPHYSICAL SECURITY CONTROLS\nThe organization provides [Assignment: 
	organization-defined personnel or roles] with initial and [Assignment: organization-defined frequency] 
	training in the employment and operation of physical security controls.\nPhysical security controls include,
	for example, physical access control devices, physical intrusion alarms, monitoring/surveillance equipment, 
	and security guards (deployment and operating procedures). Organizations identify personnel with specific 
	roles and responsibilities associated with physical security controls requiring specialized training.\nPE-
	2\nPE-3\nPE-4\nPE-5\nAT-3 (3)\nPRACTICAL EXERCISES\nThe organization includes practical exercises in 
	security training that reinforce training objectives.\nPractical exercises may include, for example, 
	security training for software developers that includes simulated cyber attacks exploiting common software 
	vulnerabilities (e.g., buffer overflows), or spear/whale phishing attacks targeted at senior 
	leaders/executives. These types of practical exercises help developers better understand the effects of such
	vulnerabilities and appreciate the need for security coding standards and processes.\nAT-3 (4)\nSUSPICIOUS 
	COMMUNICATIONS AND ANOMALOUS SYSTEM BEHAVIOR\nThe organization provides training to its personnel on [
	Assignment: organization-defined indicators of malicious code] to recognize suspicious communications and 
	anomalous behavior in organizational information systems.\nA well-trained workforce provides another 
	organizational safeguard that can be employed as part of a defense-in-depth strategy to protect 
	organizations against malicious code coming in to organizations via email or the web applications. ersonnel 
	are trained to look for indications of potentially suspicious email (e.g., receiving an unexpected email, 
	receiving an email containing strange or poor grammar, or receiving an email from an unfamiliar sender but 
	who appears to be from a known sponsor or contractor). Personnel are also trained on how to respond to such 
	suspicious email or web communications (e.g., not opening attachments, not clicking on embedded web links, 
	and checking the source of email addresses). For this process to work effectively, all organizational 
	personnel are trained and made aware of what constitutes suspicious communications. Training personnel on 
	how to recognize anomalous behaviors in organizational information systems can potentially provide early 
	warning for the presence of malicious code. Recognition of such anomalous behavior by organizational 
	personnel can supplement automated malicious code detection and protection tools and systems employed by 
	organizations.\n'
	>>> c.related_controls
	'AT-2,AT-4,PL-4,PS-7,SA-3,SA-12,SA-16'

	>>> print(c.format('json'))
	{"description": "The organization provides role-based security training to personnel with assigned security roles and 
	responsibilities:\na. Before authorizing access to the information system or performing assigned duties;\nb. When required by 
	information system changes; and\nc. [Assignment: organization-defined frequency] thereafter.", "title": "ROLE-BASED SECURITY 
	TRAINING", "responsible": "organization", "supplemental_guidance": "Organizations determine the appropriate content of security 
	training based on the assigned roles and responsibilities of individuals and the specific security requirements of organizations 
	and the information systems to which personnel have authorized access. In addition, organizations provide enterprise architects, 
	information system developers, software developers, acquisition/procurement officials, information system managers, 
	system/network administrators, personnel conducting configuration management and auditing activities, personnel performing 
	independent verification and validation activities, security control assessors, and other personnel having access to system-level 
	software, adequate security-related technical training specifically tailored for their assigned duties. Comprehensive role-based 
	training addresses management, operational, and technical roles and responsibilities covering physical, personnel, and technical 
	safeguards and countermeasures. Such training can include for example, policies, procedures, tools, and artifacts for the 
	organizational security roles defined. Organizations also provide the training necessary for individuals to carry out their 
	responsibilities related to operations and supply chain security within the context of organizational information security 
	programs. Role-based security training also applies to contractors providing services to federal agencies.", "id": "AT-3", 
	"description_intro": "The organization provides role-based security training to personnel with assigned security roles and 
	responsibilities:", "description_sections": ["a. Before authorizing access to the information system or performing assigned 
	duties;", "b. When required by information system changes; and", "c. [Assignment: organization-defined frequency] thereafter."]}

	>>> print(c.format('yaml'))
	description: 'The organization provides role-based security training to personnel
	    with assigned security roles and responsibilities:

	    a. Before authorizing access to the information system or performing assigned
	    duties;

	    b. When required by information system changes; and

	    c. [Assignment: organization-defined frequency] thereafter.'
	description_intro: 'The organization provides role-based security training to personnel
	    with assigned security roles and responsibilities:'
	description_sections:
	- a. Before authorizing access to the information system or performing assigned duties;
	- b. When required by information system changes; and
	- 'c. [Assignment: organization-defined frequency] thereafter.'
	id: AT-3
	responsible: organization
	supplemental_guidance: Organizations determine the appropriate content of security
	    training based on the assigned roles and responsibilities of individuals and the
	    specific security requirements of organizations and the information systems to
	    which personnel have authorized access. In addition, organizations provide enterprise
	    architects, information system developers, software developers, acquisition/procurement
	    officials, information system managers, system/network administrators, personnel
	    conducting configuration management and auditing activities, personnel performing
	    independent verification and validation activities, security control assessors,
	    and other personnel having access to system-level software, adequate security-related
	    technical training specifically tailored for their assigned duties. Comprehensive
	    role-based training addresses management, operational, and technical roles and
	    responsibilities covering physical, personnel, and technical safeguards and countermeasures.
	    Such training can include for example, policies, procedures, tools, and artifacts
	    for the organizational security roles defined. Organizations also provide the
	    training necessary for individuals to carry out their responsibilities related
	    to operations and supply chain security within the context of organizational information
	    security programs. Role-based security training also applies to contractors providing
	    services to federal agencies.
	title: ROLE-BASED SECURITY TRAINING

	>>> print(c.format('control-masonry'))
	description: The organization provides role-based security training to personnel with
	    assigned security roles and responsibilities&colon; a. Before authorizing access
	    to the information system or performing assigned duties; b. When required by information
	    system changes; and c. [Assignment&colon; organization-defined frequency] thereafter.
	description_intro: The organization provides role-based security training to personnel
	    with assigned security roles and responsibilities&colon;
	description_sections:
	- a. Before authorizing access to the information system or performing assigned duties;
	- b. When required by information system changes; and
	- c. [Assignment&colon; organization-defined frequency] thereafter.
	id: AT-3
	name: ROLE-BASED SECURITY TRAINING


Example code for generating list of controls in `YAML` format::

	controllist = ["AT-3", "AU-1", "IR-2"]
	d = dict()
	for id in controllist:
	    c = compliancelib.NIST800_53(id)
	    d[id] = yaml.load(c.format('yaml'))

	print(yaml.safe_dump(d, default_flow_style=False, encoding='utf-8', allow_unicode=True,
		explicit_start=True, explicit_end=True))

Example code for generating list of controls in `control-masonry` format::

	controllist = ["AT-3", "AU-1", "IR-2"]
	d = dict()
	for id in controllist:
	    c = compliancelib.NIST800_53(id)
	    d[id] = yaml.load(c.format('control-masonry'))

	print(yaml.safe_dump(d, default_flow_style=False, encoding='utf-8', allow_unicode=True,
		explicit_start=True, explicit_end=True))

To see control dependencies, simply do in python shell::

	>>> import compliancelib
	>>> cv = compliancelib.NIST800_53Viz("AU-3")
	>>> cv.precursor_controls
	['AU-3', 'AU-2', 'RA-3', 'PM-9']


Running tests
-------------

With python 2.7 (on a Mac):
(Note: you may need to include 'sudo' on a Mac, but that could also just be me)

	sudo python setup.py test
