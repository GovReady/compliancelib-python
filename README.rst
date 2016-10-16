compliancelib
=============
Machine readable cybersecurity compliance standards library for Python, starting with FISMA and NIST Risk Management Framework

Source code: https://github.com/govready/compliancelib-python/

For more history, see earlier prototype 800-53-Control-Server (https://github.com/govready/800-53-server/).

Goal
----
Create a python class that generates FISMA 800-53 security control information that can be used by other software, including:

**Essential**
- [x] control identifier, title, description, supplemental guidence etc.
- [x] list of control enhancements identifiers
- [x] control responsibility (e.g., organization or information system)
- [x] related controls

**Better**
- [ ] control assignment parameters
- [x] output control information in various formats (e.g., JSON, YAML, OpenControl)
- [x] dependent controls (precursors) and recursive dependency trees
- [x] visual representation of control dependencies

**Best**
- [x] reading OpenControl files
- [ ] resolving and reading OpenControl depencies
- [x] system compliance status (e.g., control implementation narratives)
- [ ] generating snippets for System Security Plan and other assessment artifacts
- [ ] mapping of control to (likely) generic organization role (e.g., developer, project manager, sys admin)

Warning
-------
This is pre-production and under active development.

License
-------
GPL 3.0

This was a lot of hardwork and has a number of firsts. Please support it or do not use it.

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

Running tests
-------------

With python 2.7 (on a Mac):
(Note: you may need to include 'sudo' on a Mac, but that could also just be me)

	sudo python setup.py test

With python 3.4+ (on a Mac):
(Note: you may need to include 'sudo' on a Mac, but that could also just be me)

	sudo python3 setup.py test

Usage
-----

**Basic Usage**

Using ComplianceLib is straightforward. Almost everything centers around the control identifier.

Instantiate a security control object with ComplianceLib in a Python shell::

	>>> import compliancelib
	>>> c=compliancelib.NIST800_53("AT-3")
	>>> print("The title of {} is {}".format(c.id, c.title))
	The title of AT-3 is ROLE-BASED SECURITY TRAINING

List various details of a control in a Python shell::

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
	responsibilities:\na. Before authorizing access to the information system or performing assigned duties;\nb.
	When required by information system changes; and\nc. [Assignment: organization-defined frequency] thereafter.'
	>>> c.responsible
	'organization'
	>>> c.supplemental_guidance
	'Organizations determine the appropriate content of security training based on the assigned roles and 
	responsibilities of individuals and the specific security requirements of organizations and the information 
	systems to which personnel have authorized access. In addition,  organizations provide enterprise architects,
	...
	>>> c.control_enhancements_textblock
	'\nAT-3 (1)\nENVIRONMENTAL CONTROLS\nThe organization provides [Assignment: organization-defined personnel or roles] with initial and [Assignment: organization-defined frequency] training in the employment and operation of environmental controls.\nEnvironmental controls include, for example, fire suppression and detection devices/systems, sprinkler systems, handheld fire extinguishers, fixed fire hoses, smoke detectors,
	...
	>>> c.related_controls
	['AT-2', 'AT-4', 'PL-4', 'PS-7' , 'SA-3' ,'SA-12', 'SA-16']

**Formatting**

	>>> print(c.format('json'))
	{"description": "The organization provides role-based security training to personnel with assigned security roles and 
	responsibilities:\na. Before authorizing access to the information system or performing assigned duties;\nb. When required by 
	information system changes; and\nc. [Assignment: organization-defined frequency] thereafter.", "title": "ROLE-BASED SECURITY 
	...
	responsibilities:", "description_sections": ["a. Before authorizing access to the information system or performing assigned 
	duties;", "b. When required by information system changes; and", "c. [Assignment: organization-defined frequency] thereafter."]}

	>>> print(c.format('yaml'))
	description: 'The organization provides role-based security training to personnel
	    with assigned security roles and responsibilities:

	    a. Before authorizing access to the information system or performing assigned
	    duties;

	    b. When required by information system changes; and
	...
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

**Advanced Usage - Dependencies**

ComplianceLib's `NIST800_53Viz` class creates a graph of all precursor controls for a given control. ComplianceLib is the first time these precursor controls have been made available as code.

The `NIST800_53Viz` class will also generate a graphviz file visualizing nodes and edges of the dependency graph for a security control.

The list of precursor controls are extracted from [NIST SP 800-53 R1 Assessment Cases](compliancelib/data/800-53A-R1_Assessment-Cases_All-18-Families_ipd). We extracted the precursor-controls from NIST Assessment Guide documents into simplified data structure listing precursor, concurrent, and successor controls by family. View these files in this repo's [compliancelib/data/dependencies](compliancelib/data/dependencies) subdirectory.

To see control dependencies, simply do in python shell::

	>>> import compliancelib
	>>> cv = compliancelib.NIST800_53Viz("AU-3")
	>>> cv.precursor_controls
	['AU-3', 'AU-2', 'RA-3', 'PM-9']

Creating the graphviz file is currently left as a reader exercise until future documentation completed.

Compliance as Code
---------------------

**Expressing security controls as code is useful.**
**Expressing system compliance as code is a game-changer.**

[OpenControl](http://open-control.org) is an emerging "Compliance as Code" community developing open-source, re-usable, shared compliance-by-component information and support tools. The goal is to allow developers to represent compliance as code of their component libraries and assembled systems in maintained repositories.

ComplianceLib's `OpenControlClass` and `SystemCompliance` classes work together to read OpenControl data files and represent an Information System's compliance state as a Python object that can be queried.

The `OpenControlClass` and `SystemCompliance` classes are under heavy development in ComplianceLib versions 0.8.0 through versions 0.15.0 with class attributes and methods subject to significant change.

Below is an example of using ComplianceLib to load and query compliance posture of the OpenControl [Freedonia-Compliance](https://github.com/opencontrol/freedonia-compliance) tutorial.

	>>> import compliancelib
	>>> sp = compliancelib.SystemCompliance()
	>>> sp.load_system_from_opencontrol_repo('https://github.com/opencontrol/freedonia-compliance')
	[LOG compliancelib]; INFO; 2016-10-16 11:52:52,968; opencontrolfiles; repo_url in resolve_ocfile_url: https://github.com/opencontrol/freedonia-compliance
	[LOG compliancelib]; INFO; 2016-10-16 11:52:52,968; opencontrolfiles; repo_ref in list_components_urls: https://github.com/opencontrol/freedonia-compliance
	[LOG compliancelib]; INFO; 2016-10-16 11:52:52,968; opencontrolfiles; repo_url in resolve_ocfile_url: https://github.com/opencontrol/freedonia-compliance
	[LOG compliancelib]; INFO; 2016-10-16 11:52:52,969; opencontrolfiles; ocfileurl: https://raw.githubusercontent.com/opencontrol/freedonia-compliance/master/opencontrol.yaml
	True

	>>> sp.system['name'] = "My Awesome Website"
	>>> sp.system['name']
	'My Awesome Website'

	>>> sp.control('AU-1').title
	'AUDIT AND ACCOUNTABILITY POLICY AND PROCEDURES'
	>>> sp.control('AU-1').description
	'The organization:\na. Develops, documents, and disseminates to [Assignment: organization-defined personnel or roles]:\na.1. An audit and accountability policy that addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and\na.2. Procedures to facilitate the implementation of the audit and accountability policy and associated audit and accountability controls; and\nb. Reviews and updates the current:\nb.1. Audit and accountability policy [Assignment: organization-defined frequency]; and\nb.2. Audit and accountability procedures [Assignment: organization-defined frequency].'
	>>> sp.control('AU-1').priority
	'P1'
	>>> sp.control('AU-1').implementation_status
	['implemented']
	>>> sp.control('AU-1').implementation_status_details
	{'Audit Policy': 'implemented'}
	>>> sp.control('AU-1').components
	['Audit Policy']
	>>> sp.control('AU-1').components_dict
	{'Audit Policy': [{'narrative': [{'text': 'This text describes how our organization is meeting the requirements for the\nAudit policy, and also references a more complete description at ./AU_policy/README.md\n\nSince the AU-1 `control` is to document and disseminate a policy on Audit and Accountability, then\nthis narrative suffices to provide that control. A verification step could be something\nthat checks that the referenced policy is no more than 365 days old.\n'}], 'control_key': 'AU-1', 'covered_by': [], 'standard_key': 'FRIST-800-53', 'implementation_status': 'implemented'}]}

To import a local repo:

	sp.load_system_from_opencontrol_repo('file:///fullpath/to/localfile/freedonia-compliance')

Looking at the `sp.control` object dictonary provides a glimpse of the roadmap::

	>>> sp.control('AU-1').__dict__.keys()
	dict_keys(['responsible', 'implementation_status_details', 'implementation_status', 'title', 'related_controls', 'id', 'control_enhancements', 'description_sections', 'components_dict', 'json_dict', 'assignments', 'implementation_narrative', 'family', 'description', 'control_enhancements_textblock', 'supplemental_guidance', 'components', 'description_intro', 'sg', 'priority', 'validation', 'number', 'roles'])

Adjust commandline verbosity by set log level of OpenControlFile class to one of CRITICAL, ERROR, WARNING, INFO, DEBUG::

	>>> ocf = compliancelib.OpenControlFiles()
	>>> ocf.logger.setLevel("DEBUG")
	>>> ocf.logger.setLevel("CRTICAL")

The roadmap includes emitting text snippets for System Security Plans::

	>>> sp.control_ssp_text('AU-1')
	AU-1 - AUDIT AND ACCOUNTABILITY POLICY AND PROCEDURES
	The organization:
	a. Develops, documents, and disseminates to [Assignment: organization-defined personnel or roles]:
	a.1. An audit and accountability policy that addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
	a.2. Procedures to facilitate the implementation of the audit and accountability policy and associated audit and accountability controls; and
	b. Reviews and updates the current:
	b.1. Audit and accountability policy [Assignment: organization-defined frequency]; and
	b.2. Audit and accountability procedures [Assignment: organization-defined frequency].


	responsible: organization
	roles: {}
	implementation status: ['implemented']


	via Audit Policy
	This text describes how our organization is meeting the requirements for the
	Audit policy, and also references a more complete description at ./AU_policy/README.md

	Since the AU-1 `control` is to document and disseminate a policy on Audit and Accountability, then
	this narrative suffices to provide that control. A verification step could be something
	that checks that the referenced policy is no more than 365 days old.
