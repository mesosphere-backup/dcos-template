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

import argparse
import jinja2

from . import log, mesos

class Template(object):

    def __init__(self, val):
        self.set_opts(val)
        self.get_template()

    def render(self):
        tmpl = jinja2.Template(self.source).render(data={
            "services": mesos.services()
        })
        log.debug(tmpl)
        with open(self.dest_path, "w") as fobj:
            fobj.write(tmpl)

    def set_opts(self, opts):
        try:
            self.source_path, self.dest_path, self.cmd = opts.split(":", 3)
        except:
            raise argparse.ArgumentTypeError(
                "'{0}' is not valid. It must be of the form " \
                "'source:dest:cmd'".format(opts))

    def get_template(self):
        try:
            with open(self.source_path, 'r') as fobj:
                self.source = fobj.read()
        except:
            raise argparse.ArgumentTypeError(
                "'{0}' cannot be opened. Make sure the path is valid and " \
                "you have permissions".format(self.source_path))
