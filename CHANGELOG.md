# Change Log

## compliancelib v1.1.1
- Improve OpenControl narrative parsing to handle narratives that are strings and lists

## compliancelib v1.1.0
- OpenControlFiles class generates list of dependencies by item type
- SystemCompliance class consumes content listed in dependencies (but only one level deep, e.g., will retrieve item types that are locally listed in the dependent repository, but will not recursive deeper)
- Technical debt added of possible duplicate keys read from remote repos are not tested again existing keys (e.g., a local component file and dependent component file referring to same ID for component could collide)

## complianceLib v1.0.0
- Refactor OpenControlFiles class to read components, standards, certifications from shared methods
- SystemCompliance reading standards and certificaftions
- NOTE: SystemCompliance not yet consuming content from remote dependency repos into

## compliancelib v0.13.6
- Add python logging to OpenControlFiles class

## compliancelib v0.13.4
- Indicate local repos supported in error message

## compliancelib v0.13.3
- No changes, bumping version number

## compliancelib v0.13.2
- Resolve opencontrol components on localfile system, fixing component references

## compliancelib v0.13.1
- Resolve opencontrol components on localfile system

## compliancelib v0.13.0
- Resolve opencontrol repos on localfile system

## compliancelib v0.12.2
- Correcting link in README.rst

## compliancelib v0.12.1
- Add GPL 3.0 license

## compliancelib v0.12.0
- Update README
- Represent related controls as array instead of string
- Improve tests for related control cases

## compliancelib v0.11.0
- Represent a control's enhancements as an array of control enhancement ids
- Move textblock of control enhancements into attribute control_enhancement_textblock
- Rename internal method for list of all control enhancements in 800-53

## compliancelib v0.10.0
- Changed name of `list_component*` methods

## compliancelib v0.9.0
- Add OpenControlFiles class to read open controls
- Resolve and ingest opencontrol.yaml file from GitHub repos
- Resolve and ingest OpenControl component yaml files (no dependencies)
- Update SystemCompliance class to load components via OpenControl YAML reference
- Update SystemCompliance to dump plain text write-up of NIST800-53 System Security Plan control implementation write-up
- NOTE: ingesting OpenControlFiles still incomplete

## compliancelib v0.8.0
- Add SystemCompliance class to represent System Compliance
- System Compliance class consumes OpenControl formatted component files for control implementation

## compliancelib v0.7.4
- handle control enhancement that missing data elements

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
