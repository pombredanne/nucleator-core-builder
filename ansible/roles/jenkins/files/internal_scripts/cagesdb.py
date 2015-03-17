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
import json, os
import argparse

if "CAGESDB_PATH" in os.environ:
	cagesdb_path = os.environ["CAGESDB_PATH"]
else:
	cagesdb_path = "/var/lib/jenkins"
databaseFileName = cagesdb_path+"/cagesdb.json"
# print "Reading file "+databaseFileName
def readFile():
	with open (databaseFileName, "r") as myfile:
  		data = myfile.read()
  		return data

def writeFile(data):
	with open (databaseFileName, "w") as myfile:
		myfile.write(data)
		myfile.close()

def findCustomer(cagesdb, customer_name):
	print "There are customers: "+str(len(cagesdb["customers"]))
	for cust in cagesdb["customers"]:
		if cust['name'] == customer_name:
			return cust
	return None

def findCustomerCage(customer, cage_name):
	for cage in customer["cages"]:
		if cage['name'] == cage_name:
			return cage
	return None

def findCageContainer(cage, container_name):
	for ss in cage["containers"]:
		if ss['name'] == container_name:
			return ss
	return None

def addCage(cagesdb, customer_name, cage_name):
	# print data
	customer = findCustomer(cagesdb, customer_name)
	if customer is None:
		print "Customer '"+customer_name+"' not defined, adding."
		customer = {"name": customer_name, "cages":[]}
		cagesdb["customers"].append(customer)
	cage = findCustomerCage(customer, cage_name)
	if cage is not None:
		print "Cage name '"+cage_name+"' already defined."
		return None
	customer["cages"].append({"name": cage_name, "containers":[]})
	return cagesdb

def deleteCage(cagesdb, customer_name, cage_name):
	# print data
	customer = findCustomer(cagesdb, customer_name)
	if customer is None:
		print "Customer '"+customer_name+"' not defined."
		return None
	cage = findCustomerCage(customer, cage_name)
	if cage is None:
		print "Cage name '"+cage_name+"' not defined."
		return None
	customer["cages"].remove(cage)
	return cagesdb

def addContainer(cagesdb, customer_name, cage_name, ssname, sstype):
	customer = findCustomer(cagesdb, customer_name)
	if customer is None:
		print "Customer '"+customer_name+"' not defined."
		return None
	cage = findCustomerCage(customer, cage_name)
	if cage is None:
		print "Cage name '"+cage_name+"' not defined."
		return None
	container = findCageContainer(cage, ssname)
	if container is not None:
		print "Container name '"+ssname+"' already defined."
		return None
	cage["containers"].append({"name": ssname, "type":sstype})
	return cagesdb

def deleteContainer(cagesdb, customer_name, cage_name, ssname):
	customer = findCustomer(cagesdb, customer_name)
	if customer is None:
		print "Customer '"+customer_name+"' not defined."
		return None
	cage = findCustomerCage(customer, cage_name)
	if cage is None:
		print "Cage name '"+cage_name+"' not defined."
		return None
	container = findCageContainer(cage, ssname)
	if container is None:
		print "Container name '"+ssname+"' not defined."
		return None
	cage["containers"].remove(container)
	return cagesdb

def runCageAction(action, customer, cagename):
	data = readFile()
	cagesdb = json.loads(data)
	if action == "add":
		newcagesdb = addCage(cagesdb, customer, cagename)
	elif action == "delete":
		newcagesdb = deleteCage(cagesdb, customer, cagename)

	if newcagesdb:
		newdata = json.dumps(newcagesdb, sort_keys=True, indent=4, separators=(',', ': '))
		writeFile(newdata)

def runContainerAction(action, customer_name, cagename, container):
	data = readFile()
	cagesdb = json.loads(data)
	if action == "add":
		if not "--type" in sys.argv:
			print "Usage: cagedb.py container (add, delete) --customer name --cage name --name ss_name --type ss_type"
			exit(-1)
		cc = sys.argv.index("--type")
		ss_type = sys.argv[cc+1]
		newcagesdb = addContainer(cagesdb, customer_name, cagename, container, ss_type)
	elif action == "delete":
		newcagesdb = deleteContainer(cagesdb, customer_name, cagename, container)

	if newcagesdb:
		newdata = json.dumps(newcagesdb, sort_keys=True, indent=4, separators=(',', ': '))
		# print newdata
		writeFile(newdata)

def runCageCommand(action):
	if "--custcage" in sys.argv:
		cc = sys.argv.index("--custcage")
		cuca = sys.argv[cc+1]
		ccArray = cuca.split(":")
		customer_name = ccArray[0]
		cage_name = ccArray[1]
	else:
		if not "--customer" in sys.argv:
			print "Usage: cagedb.py cage (add, delete) --customer name --cage name"
			exit(-1)
		if not "--cage" in sys.argv:
			print "Usage: cagedb.py cage (add, delete) --customer name --cage name"
			exit(-1)
		cc = sys.argv.index("--customer")
		customer_name = sys.argv[cc+1]
		cc = sys.argv.index("--cage")
		cage_name = sys.argv[cc+1]
	runCageAction(action, customer_name, cage_name)

def runSSCommand(action):
	if not "--customer" in sys.argv:
		print "Usage: cagedb.py container (add, delete) --customer name --cage name --name ss_name --type ss_type"
		exit(-1)
	if not "--cage" in sys.argv:
		print "Usage: cagedb.py container (add, delete) --customer name --cage name --name ss_name --type ss_type"
		exit(-1)
	if not "--name" in sys.argv:
		print "Usage: cagedb.py container (add, delete) --customer name --cage name --name ss_name --type ss_type"
		exit(-1)
	cc = sys.argv.index("--customer")
	customer_name = sys.argv[cc+1]
	cc = sys.argv.index("--cage")
	cage_name = sys.argv[cc+1]
	cc = sys.argv.index("--name")
	container = sys.argv[cc+1]
	runContainerAction(action, customer_name, cage_name, container)

import sys
if len(sys.argv) < 2:
	print "Usage: addCage.py action name(s)"
	print "... where action is 'cage', 'container'"
	print "(much like the nucleator cli format)"
	exit(-1)

if sys.argv[1] == "cage":
	if len(sys.argv) < 3:
		print "Usage: cagedb.py cage (add, delete) --customer name --cage name"
		exit(-1)
	runCageCommand(sys.argv[2])
elif sys.argv[1] == "container":
	if len(sys.argv) < 3:
		print "Usage: cagedb.py container (add, delete) --customer name --cage name"
		exit(-1)
	runSSCommand(sys.argv[2])
