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
import makeappjobs
# From: 
# TO: https://stash.47lining.com/projects/LIN/repos/nucleator/browse/

good = makeappjobs.testForPomXml("https://github.com/47lining/nucleator-core-builder.git", "ansible/roles/jenkins/files/sample_projects/samplewebapp/pom.xml")
print "Good" if good else "Bad"

good = makeappjobs.testForPomXml("https://github.com/47lining/nucleator-core-builder.git", "pom.xml")
print "Good" if good else "Bad"
