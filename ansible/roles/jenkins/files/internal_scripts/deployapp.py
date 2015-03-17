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
import sys, json, yaml, os
import argparse
from ebs_deploy import AwsCredentials, EbsHelper, get, out
from ebs_deploy.commands import get_command, usage

# setup arguments
parser = argparse.ArgumentParser()
parser.add_argument("working_dir", help="The working dir of the app")
parser.add_argument("argjson", help="The json")
parser.add_argument('-e', '--environment', default='sampleWebapp-env')
parser.add_argument('-v', '--archive', default='sample-webapp.war')
parser.add_argument('-l', '--version-label', help='Version label', required=False)
parser.add_argument('-w', '--dont-wait', help='Skip waiting for the init to finish', action='store_true')
parser.add_argument('-d', '--directory', help='Directory', required=False)
parser.add_argument('-f', '--log-events-to-file', help='Log events to file', required=False, action='store_true')
args = parser.parse_args()

# Read the pom.xml file
# figure out what to read from artifactory
# Send it to the cage/stackset
argdata = json.loads(args.argjson)

# Relevant bits:
# <project>
# <groupId>com.47lining.nucleator</groupId>
# <artifactId>sample-webapp</artifactId>
# <packaging>war</packaging>
# <version>1.0-SNAPSHOT</version>
# </project>
import xml.etree.ElementTree as ET
root = ET.parse(args.working_dir+"/pom.xml").getroot()
group = root.find('./{http://maven.apache.org/POM/4.0.0}groupId').text
group = group.replace("\.", "/")
artifact = root.find('./{http://maven.apache.org/POM/4.0.0}artifactId').text
packaging = root.find('./{http://maven.apache.org/POM/4.0.0}packaging').text
version = root.find('./{http://maven.apache.org/POM/4.0.0}version').text

# Load from artifactory
path = "http://10.0.2.2:8081/artifactory/simple/libs-snapshot-local/"+group+"/"+artifact+"/"+version+"/"
filename = artifact+"-"+version+"."+packaging

print "Sending "+path+filename+" to stackset "+argdata['stackset']+" in cage "+argdata['cage']

import urllib

def reporthook(a, b, c):
    print "% 3.1f%% of %d bytes\r" % (min(100, float(a * b) / c * 100), c),
url = "http://10.0.2.2:8081/artifactory/simple/libs-snapshot-local/com/47lining/nucleator/sample-webapp/1.0-SNAPSHOT/sample-webapp-1.0-20141215.215941-1.war"
file = "sample-webapp.war"
urllib.urlretrieve(url, file, reporthook)
print
#
# ebs-deploy deploy --environment sampleWebapp-env --archive target/sample-webapp.war

# from ebs-deploy:
command_name = "deploy"
command = get_command(command_name)

from boto import set_stream_logger
set_stream_logger('boto')

# load config
#f = open(args.config_file, 'r')
with open(args.working_dir+"/ebs.config", 'r') as f:
    contents = f.read()
contents_with_environment_variables_expanded = os.path.expandvars(contents)
config = yaml.load(contents_with_environment_variables_expanded)

# create credentials
aws = AwsCredentials(
    get(config, 'aws.access_key',       os.environ.get('AWS_ACCESS_KEY_ID')),
    get(config, 'aws.secret_key',       os.environ.get('AWS_SECRET_ACCESS_KEY')),
    get(config, 'aws.region',           os.environ.get('AWS_DEFAULT_REGION')),
    get(config, 'aws.bucket',           os.environ.get('AWS_BEANSTALK_BUCKET_NAME')),
    get(config, 'aws.bucket_path',      os.environ.get('AWS_BEANSTALK_BUCKET_NAME_PATH')))

# create helper
helper = EbsHelper(aws, app_name=get(config, 'app.app_name'))

# execute the command
exit(command.execute(helper, config, args))
