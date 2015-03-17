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
ApplicationType=beanstalk
ApplicationFlavor=java
ApplicationName=UnitTestApp
GitRepoPath=https://github.com/47lining/nucleator-core-builder.git
GitCredentials=d780f411-5666-4fce-a0dd-8e1a1dc1de2d
PomPath=jenkins/sample_projects/samplewebapp/pom.xml
NUI_URL=http://nucleator-ui.build.47lining.com:8080
NUI_USER=admin
python ../internal_scripts/makeappjobs.py $ApplicationType $ApplicationFlavor $ApplicationName $GitRepoPath $GitCredentials $PomPath