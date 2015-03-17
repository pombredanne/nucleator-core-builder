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
function myFunction() {
  span = document.createElement("span");
  span.innerHTML = "&copy; Copyright 2015, 47Lining, LLC";
  f = document.getElementById('footer');
  f.insertBefore(span, f.firstChild);

  ul = document.getElementById('breadcrumbs');
  li = ul.getElementsByTagName('li');
  anchor = li[0].getElementsByTagName("a");
  anchor[0].innerHTML = "Nucleator";

  head = document.getElementsByTagName('head');
  title = head[0].getElementsByTagName('title');
  title[0].innerHTML = title[0].innerHTML.replace("Jenkins", "Nucleator");
  links = head[0].getElementsByTagName('link');
  for (var i in links) {
     link = links[i];
     if (link.getAttribute('rel') == 'shortcut icon') {
        link.setAttribute('href', '/userContent/favicon.ico');
        break;
     }
  }
};
var body = document.getElementsByTagName('body');
if (window.addEventListener) {
  window.addEventListener('load', myFunction, false);
}
else if (window.attachEvent) {
  window.attachEvent('onload', myFunction );
}