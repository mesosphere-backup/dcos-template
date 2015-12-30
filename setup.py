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

import imp
import os
import sys

# Get the version without needing to install `mesos.cli`. Note that this must
# be deleted from sys.modules for nosetests to run correctly.
mod = imp.load_source(
    'dcos_template',
    os.path.join(os.path.dirname(__file__), "dcos_template", "__init__.py")
)
version = mod.__version__
del sys.modules["dcos_template"]

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    readme = f.read()

requires = [
    "ConfigArgParse >= 0.10.0",
    "jinja2 >= 2.7.3",
    "requests >= 2.2.1"
]

config = {
    'name': 'dcos-template',
    'version': version,
    'description': 'Template generation for DCOS clusters',
    'long_description': readme,
    'author': 'Thomas Rampelberg',
    'author_email': 'thomas@mesosphere.io',
    'url': 'http://pypi.python.org/pypi/dcos-template',
    'license': 'Apache 2.0',
    'keywords': 'dcos',
    'classifiers': [],

    'packages': [
        'dcos_template'
    ],
    'entry_points': {
        'console_scripts': [
            'dcos-template = dcos_template.main:main'
        ]
    },
    'install_requires': requires,
    'test_suite': 'nose.collector',
    'scripts': [
    ]
}

if __name__ == "__main__":
    from setuptools import setup

    setup(**config)
