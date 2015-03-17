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

#
#  $ApplicationType $ApplicationName $GitRepoPath $GitCredentials $PomPath
#
#  Template Vars:
#  - $ApplicationName
#  - $ApplicationFlavor
#  - $ApplicationType
#  - $GitRepoPath
#  - $GitCredentials
#  - $PomPathOnly (for SparseCheckoutPath)
#  - $PomPath
#  - $GroupId
#  - $ArtifactId
# 

def fixupFile(filename, config_xml):
    #
    # fixup job template
    #
    ApplicationType = sys.argv[2]
    ApplicationFlavor = sys.argv[3]
    ApplicationName = sys.argv[4]
    GitRepoPath = sys.argv[5]
    GitCredentials = sys.argv[6]
    PomPath = sys.argv[7]
    PomPathOnly = os.path.dirname(PomPath)
    #
    s = Template(config_xml)
    job_def = s.substitute(
        ApplicationType = ApplicationType,
        ApplicationFlavor = ApplicationFlavor,
        ApplicationName = ApplicationName,
        GitRepoPath = GitRepoPath,
        GitCredentials = GitCredentials,
        PomPath = PomPath,
        PomPathOnly = PomPathOnly
    )
    jenkins_url = None
    if "JENKINS_URL" in os.environ:
        jenkins_url = os.environ["JENKINS_URL"]
    else:
        print "JENKINS_URL environment variable must be set."
        exit(1)
    jenkins_user = None
    if "NUI_USER" in os.environ:
        jenkins_user = os.environ["NUI_USER"]
    jenkins_password = None
    if "NUI_PWD" in os.environ:
        jenkins_password = os.environ["NUI_PWD"]
    print "Connection: "+jenkins_url+" ("+jenkins_user+")"
    try:
        api = Jenkins(jenkins_url, jenkins_user, jenkins_password)
    except:
        api = Jenkins(jenkins_url)

    filenames = filename.split(".")
    project_name = filenames[0]+" "+ApplicationName
    print "Creating project '"+project_name+"'"
    job = api.create_job(project_name, job_def)

    # view = api.views["StackSets"]
    # if view is None:
        # api.views.create("StackSets")
    # view.add_job(project_name, job)
    # print("Project created - "+job.name+" and added to the 'StackSets' view.")

if __name__ == '__main__':
    if (len(sys.argv) < 7):
        print "Usage: python filename makeappjobs.py $ApplicationType $ApplicationFlavor $ApplicationName $GitRepoPath $GitCredentials $PomPath"
        exit(1)
    # print "Cage "+cage_name
    # path = os.environ['JENKINS_HOME']
    job = sys.argv[1] # beanstalk:flavor
    with open (job, "r") as myfile:
        xml=myfile.read()
    fixupFile(os.path.basename(job), xml)
