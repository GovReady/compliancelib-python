# Generates YAML files for use with the GovReady Knowledge Base.

from collections import OrderedDict
import re
from urllib import urlencode

import rtyaml # this needs to be pip-installed!

import compliancelib

def make_resource_id(control_id):
	x = re.sub(r"\s+", "", control_id)
	x = re.sub(r"[^A-Za-z0-9]", "-", x)
	x = x.strip("- ")
	x = "nist-800-53-control-" + x.lower()
	return x

ids = \
	list(compliancelib.NIST800_53.get_control_ids()) \
  + list(compliancelib.NIST800_53.get_control_enhancement_ids())

resources = []

for c in ids:
	cc = compliancelib.NIST800_53(c)

	is_enhancement = False
	if "(" in c: # ha that's not great but OK
		is_enhancement = True
		parent_control = compliancelib.NIST800_53(c.rsplit(" (", 1)[0])

	res = OrderedDict([
		("id", make_resource_id(c)),
		("type", "control"),
		("enhancement", is_enhancement),
		("generator", "compliancelib"),
		("owner", "NIST"),
		("title", cc.number + " " + cc.title),
		("alt-titles", [cc.number, cc.title]),
		("short-title", cc.number),
		("description", cc.description),
		("family", cc.family if not is_enhancement else parent_control.family),
		("description", cc.description or ""), # must not be null
		("supplemental-guidance", cc.supplemental_guidance),
		("url", "http://800-53.govready.com/control?" + urlencode({ "id": cc.id })),
	])

	if is_enhancement:
		res["parent-control"] = parent_control.id

	resources.append(res)

print(rtyaml.dump_all(resources))
