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
from jenkinsapi.utils.requester import Requester
from string import Template
import sys, os, httplib

#
#  $ApplicationType $ApplicationName $GitRepoPath $PomPath
#
#  Template Vars:
#  - $ApplicationName
#  - $ApplicationFlavor
#  - $ApplicationType
#  - $GitRepoPath
#  - $PomPathOnly (for SparseCheckoutPath)
#  - $PomPath
#  - $GroupId
#  - $ArtifactId
# 

def fixupFile(filename, config_xml):
    #
    # fixup job template
    #
    ApplicationType = sys.argv[1]
    ApplicationFlavor = sys.argv[2]
    ApplicationName = sys.argv[3]
    GitRepoPath = sys.argv[4]
    PomPath = sys.argv[5]
    ArtifactoryUrl = sys.argv[6]
    PomPathOnly = os.path.dirname(PomPath)
    #
    s = Template(config_xml)
    job_def = s.substitute(
        ApplicationType = ApplicationType,
        ApplicationFlavor = ApplicationFlavor,
        ApplicationName = ApplicationName,
        GitRepoPath = GitRepoPath,
        PomPath = PomPath,
        ArtifactoryUrl = ArtifactoryUrl,
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

    if jenkins_password is None or jenkins_user is None:
        api = Jenkins(jenkins_url, requester = Requester(baseurl=jenkins_url, ssl_verify=False))
    else:
        # If authentication is not turned on, this call raises an exception
        try:
            api = Jenkins(jenkins_url, jenkins_user, jenkins_password, requester = Requester(username=jenkins_user, password=jenkins_password, baseurl=jenkins_url, ssl_verify=False))
        except:
            api = Jenkins(jenkins_url, requester = Requester(baseurl=jenkins_url, ssl_verify=False))
    filenames = filename.split(".")
    project_name = filenames[0]+" "+ApplicationName
    print "Creating project '"+project_name+"'"
    job = api.create_job(project_name, job_def)

def validatePomPath(host, repo, path, ApplicationFlavor, branch):
    import shutil, shlex
    shutil.rmtree(repo, ignore_errors=True)
    import subprocess
    # ssh://stash.47lining.com:7999/lin/nucleator-core-builder.git
    cmd = "git clone "+host
    print "Cloning into '"+path+"'...\n"
    subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
    os.chdir(repo)
    if branch:
        cmd = "git checkout "+branch
        print "Changing to branch '"+branch+"'...\n"
        subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
    # print "Checking for "+repo+"/"+path
    if ApplicationFlavor == 'java':
        isthere = os.path.isfile(path)
    else:
        isthere = os.path.isdir(path)
    os.chdir("..")
    shutil.rmtree(repo, ignore_errors=True)
    return isthere

def testForPomXml(GitRepoPath, PomPath, ApplicationFlavor, branch):
    if 'stash' in GitRepoPath:
        return testForPomXmlStash(GitRepoPath, PomPath, ApplicationFlavor, branch)
    if 'github' in GitRepoPath:
        return testForPomXmlGitHub(GitRepoPath, PomPath, ApplicationFlavor, branch)
    print "Unsupported Git repo"
    exit(1)

def testForPomXmlStash(GitRepoPath, PomPath, ApplicationFlavor, branch):
    import re, urllib2, json
    git_pattern = re.compile('ssh:\/\/[a-zA-Z0-9.]*\@?([a-zA-Z0-9/.-]+?):?[0-9]*\/([a-zA-Z0-9/.-]+?)\/([a-zA-Z0-9.-]+)\.git')
    m = git_pattern.match(GitRepoPath)
    if m is None:
        print "'"+GitRepoPath+"' doesn't match pattern."
        return False
    host = m.group(1)
    print "Host: "+ host
    project = m.group(2)
    print "Project: "+ project
    repo = m.group(3)
    print "Repo: "+repo
    return validatePomPath(GitRepoPath, repo, PomPath, ApplicationFlavor, branch)

# From: https://github.com/47lining/nucleator-core-builder.git
# TO: https://raw.githubusercontent.com/47lining/nucleator-core-builder/master/LICENSE
#
# This is still in progress.
#
def testForPomXmlGitHub(GitRepoPath, PomPath, ApplicationFlavor, branch):
    import re, urllib2, json
    git_pattern = re.compile('https:\/\/([a-zA-Z0-9/.-]+):?[0-9]*\/([a-zA-Z0-9/.-]+?)\/([a-zA-Z0-9.-]+)\.git')
    m = git_pattern.match(GitRepoPath)
    if m is None:
        print "'"+GitRepoPath+"' doesn't match pattern."
        return False
    host = m.group(1)
    print "Host: "+ host
    project = m.group(2)
    print "Project: "+ project
    repo = m.group(3)
    print "Repo: "+repo
    return validatePomPath(GitRepoPath, repo, PomPath, ApplicationFlavor, branch)

#
# When going thru the list of jobs, ignore -java if we're python
# Delete -python at the end of the name
#
if __name__ == '__main__':
    if (len(sys.argv) < 7):
        print "Usage: python makeappjobs.py $ApplicationType $ApplicationFlavor $ApplicationName $GitRepoPath $PomPath $ArtifactoryUrl"
        exit(1)
    ApplicationType = sys.argv[1] # beanstalk
    ApplicationFlavor = sys.argv[2] # beanstalk:flavor
    GitRepoPath = sys.argv[4]
    PomPath = sys.argv[5]
    branch = None
    if len(sys.argv)==8:
        branch = sys.argv[7]
    if not testForPomXml(GitRepoPath, PomPath, ApplicationFlavor, branch):
        print "Please check spelling of repo and/or path to pom."
        exit(1)
    import __main__ as main
    print(main.__file__)
    path = os.path.dirname(main.__file__)  # the jenkins/scripts dir
    jobspath = path+"/../jobs/"+ApplicationType+" app/"
    jobfiles = os.listdir(jobspath)
    for job in jobfiles:
        filename = os.path.basename(job)
        if '-' in filename and not filename.endswith("-"+ApplicationFlavor+".xml"):
            continue
        with open (jobspath+job, "r") as myfile:
            xml=myfile.read()
        if filename.endswith("-"+ApplicationFlavor+".xml"):
            filename = filename.replace("-"+ApplicationFlavor, '')
        fixupFile(filename, xml)
