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
#
# fixup-config.py
import sys, json, yaml, os
# import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

xmlfile = ElementTree.parse("config.xml")
root = xmlfile.getroot()
auth_strategy = root.find('./authorizationStrategy')
#
# attribute change: class="hudson.security.GlobalMatrixAuthorizationStrategy
auth_strategy.attrib["class"] = "hudson.security.GlobalMatrixAuthorizationStrategy"

# Check if they are there or not:
permissions = auth_strategy.find('./permission')
if permissions is None:
	# for each line in persmissions-list.txt, add child node <permission>{{name}}:admin</permission>
	#
	with open ("permissions-list.txt", "r") as myfile:
		perms = myfile.readlines()
	for permission in perms:
		p = SubElement(auth_strategy, "permission")
		p.text = permission.strip('\n')+":admin"
	# Additional permissions for anonymous to enable
	# the ansible-jenkins role to run after security
	# has been turned on.
	p = SubElement(auth_strategy, "permission")
	p.text = "hudson.model.Hudson.Read:anonymous"

security_realm = root.find('./securityRealm')
#
# attribute change to class="hudson.security.HudsonPrivateSecurityRealm"
security_realm.attrib["class"] = "hudson.security.HudsonPrivateSecurityRealm"

# add children: <disableSignup>true</disableSignup>
#     <enableCaptcha>false</enableCaptcha>
#
# Check if they are there or not:
disableSignup = security_realm.find('./disableSignup')
if disableSignup is None:
	p = SubElement(security_realm, "disableSignup")
	p.text = "true"
	p = SubElement(security_realm, "enableCaptcha")
	p.text = "false"

remember_me = root.find('./disableRememberMe')
#
# change text to true
#
remember_me.text = "true"

#
# write it back out.
xmlfile.write("config-1.xml")