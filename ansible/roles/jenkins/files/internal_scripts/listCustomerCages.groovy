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
import groovy.io.FileType
def parent_path = "/var/lib/jenkins/siteconfig/ansible/roles/siteconfig"
def list = []
def pattern = ~/([a-zA-Z0-9]+)-([a-zA-Z0-9]+).yml/

def dir = new File(parent_path+"/vars")
dir.eachFileRecurse (FileType.FILES) { file ->
  def mat = pattern.matcher(file.name)
  if(mat.matches() && !file.name.startsWith("{")) {
      println "CustomerCage: "+mat[0][1]+":"+mat[0][2]
	  list << mat[0][1]+":"+mat[0][2]
  }
}
return list
