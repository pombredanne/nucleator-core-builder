import os, yaml
from nucleator.cli import properties

# Read sources.yml
# find the src= for   name: siteconfig
# TODO handle version?
import yaml

sources = os.path.join(properties.NUCLEATOR_CONFIG_DIR, "sources.yml")

stream = open(sources, 'r')
slist = yaml.load(stream)
for sname in slist:
	if sname['name'] == "siteconfig":
		print sname['src']
		exit(0)
exit(1)
