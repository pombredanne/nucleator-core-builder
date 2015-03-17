/*
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
*/
//versions.groovy

//Given:
//- artifactory URL
//- group id
//- artifact id

artifactory_host = "10.0.203.83"
artifactory_port = "8081"
group = "com.47lining.nucleator"
artifact = "sample-webapp"

url = "http://"+artifactory_host+":"+artifactory_port+"/artifactory/api/search/gavc?g="+group+"&a="+artifact
println "Reading "+url
def data = new URL(url).getText(requestProperties: ['X-Result-Detail': 'info'])
def slurper = new groovy.json.JsonSlurper()
def a_fact = slurper.parseText(data)
//println "Result: "+data
println "Result count: "+a_fact.results.size()
def result = []
def pattern = ~/http:\/\/[a-zA-Z0-9.]*:?[0-9]*\/artifactory\/([a-zA-Z-]+)\/$group\/$artifact\/([a-zA-Z0-9.-]+)\/$artifact-(.*).war/
//println "Matches: "+pattern.matcher("http://10.0.203.83:8081/artifactory/libs-snapshot-local/com/47lining/nucleator/sample-webapp/1.0-SNAPSHOT/sample-webapp-1.0-20141215.215941-1.war").matches()
//
a_fact.results.each{
	println "Props DL: "+it.downloadUri
	def mat = pattern.matcher(it.downloadUri)
	println "URL Match"+mat.matches()
	println "Repo: "+mat[0][1]
	println "Version: "+mat[0][2]
	println "File: "+mat[0][3]
	println "Props CS: "+it.checksums.md5
	println "Props LM: "+it.lastModified
	result.add(it.downloadUri)
}
return result
