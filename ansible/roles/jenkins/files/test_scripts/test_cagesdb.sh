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
export CAGESDB_PATH=`dirname "$BASH_SOURCE"`
echo "Adding cage qa:unittest"
python ../scripts/cagesdb.py cage add --customer qa --cage unittest
echo "Adding duplicate cage qa:unittest"
python ../scripts/cagesdb.py cage add --customer qa --cage unittest
echo "Deleting nonexistant cage qa:ci"
python ../scripts/cagesdb.py cage delete --customer qa --cage ci
echo "Deleting cage qa:unittest"
python ../scripts/cagesdb.py cage delete --customer qa --cage unittest

echo "Adding container qa:unittest:builder:beanstalk:java"
python ../scripts/cagesdb.py cage add --customer qa --cage unittest
python ../scripts/cagesdb.py container add --customer qa --cage unittest --name builder --type beanstalk:java
echo "Deleting container qa:unittest:builder:beanstalk:java"
python ../scripts/cagesdb.py container delete --customer qa --cage unittest --name builder
python ../scripts/cagesdb.py cage delete --customer qa --cage unittest
