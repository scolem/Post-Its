"""
Copyright 2014 Scott Lemmer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

#update time and create the next default directory

import datetime
import os

timestamp=datetime.datetime.now().strftime('%y%m%d%H')
print timestamp
myfile=open("timelog.txt", "a")
myfile.write("\n"+timestamp)
myfile.close()

try:
    os.mkdir(timestamp)
except OSError:
    print "Error: The file already exists"
