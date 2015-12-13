# Change Log

## compliancelib v0.7.3
- replace xml.etree.ElementTree with defusedxml.ElementTree
- remove unused imports

## compliancelib v0.7.2
- Improve json nosetest
- rename test files to nist800_53 convention
- compliancelib.NIST800_53Viz v0.3.1
	- Use 2to3 to upgrade nist800_53.py to Python3

## compliancelib v0.7.0
ALERT: Renaming of SecControl to NIST800_53
- Rename compliancelib.SecControl to compliancelib.NIST800_53
- Rename compliancelib.SecControlViz to compliancelib.NIST800_53Viz

## compliancelib v0.6.1
- Correct changelog of compliancelib v0.6.0

## compliancelib v0.6.0
- compliancelib.SecControl v0.7.0
	- Add `format` method to produce `JSON`, `YAML`, `Control-Masonry` format
- compliancelib.SecControlViz v0.2.0
	- no changes

## compliancelib v0.5.0
- compliancelib.SecControl v0.6.0
	- no changes
- compliancelib.SecControlViz v0.2.0
	- Add attribute `precursor_controls`

## compliancelib v0.4.2
- compliancelib.SecControl v0.6.0
	- Remove `xsltproc` dependency, parse XML with Python `xml.etree.ElementTree`
	- Add CHANGELOG.md file
	- README improvements
