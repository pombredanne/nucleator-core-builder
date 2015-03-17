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
import re, sys

url_pattern = re.compile('https?:\/\/[a-zA-Z0-9.]+:?[0-9]*\/artifactory\/[a-zA-Z0-9/.-]+?\/([a-zA-Z0-9.-]+)\/[a-zA-Z0-9.-]+\.war')
if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print "Usage: python parseUrl.py $WarUrlPath"
        exit(1)
    m = url_pattern.match(sys.argv[1])
    if m is None:
        print "'"+sys.argv[1]+"' doesn't match pattern."
        exit(1)
    print m.group(1)
