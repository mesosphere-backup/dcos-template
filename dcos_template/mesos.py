# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import itertools
import requests

from . import log


# XXX - Make this configurable
TIMEOUT = 5

# {
#     "services": [
#         {
#             "name": "derp",
#             "tasks": [
#                 {
#                     "ip": "127.0.1.1",
#                     "port": 31261
#                 }
#             ]
#         }
#     ]
# }

# XXX - Should cache this
@log.duration
def fetch():
    try:
        # XXX - Make the mesos source configurable.
        return requests.get(
            "http://leader.mesos:5050/master/state",
            timeout=TIMEOUT).json()
    except requests.exceptions.ConnectionError:
        log.fatal("Could not get state.json")

def get_task_data(task):
    return {
        "ip": task.get("statuses", [])[-1].get("container_status").get(
            "network_infos")[0].get("ip_addresses")[0].get("ip_address"),
        "port": int(task.get("resources").get("ports").split("-")[0][1:])
    }

def services():
    tasks = [x for y in
        [fwk.get("tasks") for fwk in fetch().get("frameworks")] for x in y]
    return [{
        "name": name,
        "tasks": map(get_task_data, data)
    } for name, data in itertools.groupby(tasks,
        key=lambda x: x.get("name", None))]
