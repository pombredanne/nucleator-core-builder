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
from jenkinsapi.jenkins import Jenkins
from string import Template
import sys, os

if __name__ == '__main__':
    if (len(sys.argv) < 4):
        # python $REPO_HOME/scripts/makejob.py "$StacksetType" "$CageName"
        print "Usage: python makejob.py <host> <stackset type> <cagename>"
        exit(1)
    jenkins_url = sys.argv[1]
    stackset_type = sys.argv[2]
    # print "SST "+stackset_type
    cage_name = sys.argv[3]
    # print "Cage "+cage_name
    path = os.environ['JENKINS_HOME']
    with open (path+"/workspace/CheckoutTheGitRepo/jenkins/jobs/"+stackset_type+"/config.xml", "r") as myfile:
        xml=myfile.read()
    #
    # fixup job template
    #
    s = Template(xml)
    job_def = s.substitute(cage_name=cage_name, stackset_type=stackset_type)
    api = Jenkins(jenkins_url)
    project_name = "Create a \""+stackset_type+"\" in \""+cage_name+"\" cage"
    print "Creating project '"+project_name+"'"
    job = api.create_job(project_name, job_def)

    view = api.views["StackSets"]
    if view is None:
        api.views.create("StackSets")
    view.add_job(project_name, job)
    print("Project created - "+job.name+" and added to the 'StackSets' view.")
