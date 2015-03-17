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
from jenkinsapi.view import View
import os, sys, logging

# Create a view if it doesn't exist

def readFile(filename):
    with open (filename, "r") as myfile:
        return myfile.read()

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print "Usage: python jenkins.py <jenkins-host> <action> <name> <file>"
        exit(1)
    jenkins_url = sys.argv[1]
    if sys.argv[2] == "wait-for-ready":
        if (len(sys.argv) > 3):
            timeout = int(sys.argv[3])
        else:
            timeout = 10
        import urllib2, time
        now = time.time()
        start = time.time()
        while (now - start < timeout):
            try:
                # The admin user may not really exist, but we're just checking
                # for system availability
                print "Pinging "+jenkins_url+"/user/admin/"
                urllib2.urlopen(jenkins_url+"/user/admin/").read()
                # if it actually comes back, we're good
                exit(1)
            except:
                print "Got exception, sleeping..."
                time.sleep(0.5)
            now = time.time()
        exit(0)
    jenkins_user = None
    if "NUI_USER" in os.environ:
        jenkins_user = os.environ["NUI_USER"]

    jenkins_password = None
    if "NUI_PWD" in os.environ:
        jenkins_password = os.environ["NUI_PWD"]
    '''
    This is untested and added if the ansible service restart doesn't work.
    if sys.argv[2] == "safe-restart":
        # Need to post to http://jenkins.build.47lining.com:8080/safeRestart with basic auth
        import urllib2
        if jenkins_user is not None:
            # Create an OpenerDirector with support for Basic HTTP Authentication...
            auth_handler = urllib2.HTTPBasicAuthHandler()
            auth_handler.add_password(realm='Jenkins',
                                      uri=jenkins_url,
                                      user=jenkins_user,
                                      passwd=jenkins_password)
            opener = urllib2.build_opener(auth_handler)
            # ...and install it globally so it can be used with urlopen.
            urllib2.install_opener(opener)
        # send data to force a POST
        try:
            req = urllib2.urlopen(jenkins_url+'/safeRestart', data="1")
        except:
            # "normal" is a 503 - service unavailable
            pass
        # print req.getcode()
        exit(0)
    '''
    if jenkins_password is None or jenkins_user is None:
        api = Jenkins(jenkins_url, requester = Requester(baseurl=jenkins_url, ssl_verify=False))
    else:
        # If authentication is not turned on, this call raises an exception
        try:
            api = Jenkins(jenkins_url, jenkins_user, jenkins_password, requester = Requester(username=jenkins_user, password=jenkins_password, baseurl=jenkins_url, ssl_verify=False))
        except:
            api = Jenkins(jenkins_url, requester = Requester(baseurl=jenkins_url, ssl_verify=False))

    if sys.argv[2]=="create-view":
        if (len(sys.argv) < 4):
            print "Usage: python jenkins.py <host> create-view <name>"
            exit(1)
        for i in range(3, len(sys.argv)):
            view = api.views.create(sys.argv[i])
            if view is not None:
                print "View '"+sys.argv[i]+"' created."
    elif sys.argv[2]=="add-job-to-view":
        if (len(sys.argv) < 5):
            print "Usage: python jenkins.py <host> addjobtoview <viewname> <jobname>"
            exit(1)
        view = api.views[sys.argv[3]]
        if view is None:
            print "View '"+sys.argv[3]+"' not found"
            exit(1)
        if sys.argv[4] not in api.jobs:
            print "Job '"+sys.argv[4]+"' not found"
            exit(1)
        job = api.jobs[sys.argv[4]]
        view.add_job(sys.argv[4], job)
        print "Job added to view"
    elif sys.argv[2] == "create-job":
        if (len(sys.argv) < 5):
            print "Usage: python jenkins.py <host> create-job <name> <file>"
            exit(1)
        if sys.argv[3] in api.jobs:
            print "Job '"+sys.argv[3]+"' already exists"
        else:
            xml = readFile(sys.argv[4])
            job = api.create_job(sys.argv[3], xml)
            print("Job created - "+job.name)
    elif sys.argv[2] == "create-job-add-to-view":
        if (len(sys.argv) < 6):
            print "Usage: python jenkins.py <host> create-job-add-to-view <view> <name> <file>"
            exit(1)
        if sys.argv[4] in api.jobs:
            job = api.jobs[sys.argv[4]]
            print "Job '"+sys.argv[4]+"' already exists"
        else:
            xml = readFile(sys.argv[5])
            job = api.create_job(sys.argv[4], xml)
            print("Job created - "+job.name)
        api.views[sys.argv[3]].add_job(sys.argv[4], job)
        print "Job added to view"
    elif sys.argv[2] == "run-job":
        if (len(sys.argv) < 4):
            print "Usage: python jenkins.py <host> run-job <name>"
            exit(1)
        if sys.argv[3] not in api.jobs:
            print "Job '"+sys.argv[3]+"' not found"
            exit(1)
        job = api.jobs[sys.argv[3]]
        try:
            old_level = logging.getLogger().getEffectiveLevel()
            logging.disable(logging.ERROR)
            job.invoke()
            logging.disable(old_level)
        except:
            # It sometimes throws a 404 querying the queue...
            # The playbook has ignore_errors: true
            # but if the console has ERROR it says the build is unsuccessful.
            pass
        print("Job invoked - "+job.name)
    else:
        print "Unknown command."
