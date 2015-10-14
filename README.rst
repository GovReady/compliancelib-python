compliancelib
=============
A python package extracted from prototype 800-53-Control-Server (https://github.com/govready/800-53-server)

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
- xsltproc - to perform XSL transformations
- PyYAML - to generate YAML

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

    >>> import compliancelib
    >>> c=compliancelib.SecControl("AC-1")
    >>> c.id
    'AC-1'
    >>> c.title
    u'ACCESS CONTROL POLICY AND PROCEDURES'
