# compliancelib-python
Machine readable cybersecurity compliance standards library for Python, starting with FISMA and NIST Risk Management Framework

Source code: https://github.com/govready/compliancelib-python

For more history, see earlier prototype 800-53-Control-Server (https://github.com/govready/800-53-server).

## Goal
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
- [ ] mapping of control to (likely) generic organization role (e.g., developer, project manager, sys admin)
- [x] reading OpenControl files
- [ ] resolving and reading OpenControl depencies
- [x] system compliance status (e.g., control implementation narratives)
- [ ] generating snippets for System Security Plan and other assessment artifacts

## Warning
This is pre-production and under active development.

## Requirements
- Python 2.7 or 3.4+
- PyYAML
- graphviz
- defusedxml

## Installation
Compliancelib can be installed with Python pip

```
pip install compliancelib
```
To install Python pip:

- https://pip.pypa.io/en/stable/installing/
- http://sharadchhetri.com/2014/05/30/install-pip-centos-rhel-ubuntu-debian/

Compliancelib can beinstalled with Python Easy Install

```
    easy_install compliancelib
```

## Usage

**Basic Usage**

Using ComplianceLib is straightforward. Almost everything centers around the control identifier.

Instantiate a security control object with ComplianceLib in a Python shell:

```python
>>> import compliancelib
>>> c = compliancelib.NIST800_53("AT-3")
>>> print("The title of {} is {}".format(c.id, c.title))
The title of AT-3 is ROLE-BASED SECURITY TRAINING
```

List various details of a control in a Python shell:
```
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
```

**Formatting**

ComplianceLib will also generate control information in various formats.

```
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
```

Example code for generating list of controls in `YAML` format

```python
controllist = ["AT-3", "AU-1", "IR-2"]
d = dict()
for id in controllist:
    c = compliancelib.NIST800_53(id)
    d[id] = yaml.load(c.format('yaml'))

print(yaml.safe_dump(d, default_flow_style=False, encoding='utf-8', allow_unicode=True,
    explicit_start=True, explicit_end=True))
```

Example code for generating list of controls in `control-masonry` format

```python
controllist = ["AT-3", "AU-1", "IR-2"]
d = dict()
for id in controllist:
    c = compliancelib.NIST800_53(id)
    d[id] = yaml.load(c.format('control-masonry'))

print(yaml.safe_dump(d, default_flow_style=False, encoding='utf-8', allow_unicode=True,
    explicit_start=True, explicit_end=True))

```

**Advanced - Dependencies**

To see control dependencies, simply do in python shell::

```python
>>> import compliancelib
>>> cv = compliancelib.NIST800_53Viz("AU-3")
>>> cv.precursor_controls
['AU-3', 'AU-2', 'RA-3', 'PM-9']
```

## Running tests

With python 2.7 (on a Mac):
(Note: you may need to include 'sudo' on a Mac, but that could also just be me)

```
sudo python setup.py test
```

With python 3.4+ (on a Mac):
(Note: you may need to include 'sudo' on a Mac, but that could also just be me)

```
sudo python3 setup.py test
```
