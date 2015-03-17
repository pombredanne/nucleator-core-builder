# Copyright 2015 47Lining LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os, yaml
from nucleator.cli import properties

# Read sources.yml
# find the src= for   name: siteconfig
# TODO handle version?

# Change 1: strip off leading git+.  That prefix is added for ansible_galaxy
# but not supported by Jenkins' Git plugin
# per @semifocused

import yaml

sources = os.path.join(properties.NUCLEATOR_CONFIG_DIR, "sources.yml")

stream = open(sources, 'r')
slist = yaml.load(stream)
for sname in slist:
	if sname['name'] == "siteconfig":
		src = sname['src']
		if src.startswith("git+"):
			src = src[4:]
		print src
		exit(0)
exit(1)
