# -*- coding: utf-8 -*-
#
# Copyright 2015 FUJITSU LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import string
import random
import json

from tempest import test
from tempest.api.monitoring import base


class Waiter(base.BaseLogsTestCase):
    def run_and_wait(self, sid, message, headers=None):

        def wait():
            return self.logs_search_client.count_search_messages(sid) > 0

        self.assertEqual(0, self.logs_search_client.count_search_messages(sid),
                         'Find log message in elasticsearch: {0}'.format(sid))

        if not headers:
            headers = dict()

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
            message = json.dumps(dict(message=message))
        self.logs_client.send_single_log(message, headers)

        # wait - retry every 1 sec with timeout 10 sec
        test.call_until_true(wait, 10, 1)
        response = self.logs_search_client.search_messages(sid)
        self.assertEqual(1, len(response))

        return response


class LogsApiTestJSON(base.BaseLogsTestCase):
    _interface = 'json'

    def test_single_log(self):
        message = json.dumps(dict(message='test logs'))
        headers = dict()
        headers['Content-Type'] = 'application/json'
        response, _ = self.logs_client.send_single_log(message, headers)
        self.assertEqual('204', response['status'])


class LogsSearchTestJSON(base.BaseLogsTestCase):
    _interface = 'json'

    def test_connection(self):
        response, body = self.logs_search_client.get_metadata()
        self.assertEqual('200', response['status'])
        self.assertEqual(200, body['status'])


class SingleLogConnection(Waiter):

    def test_small_message(self):
        self.run_and_wait(*_generate_unique_message(size=10))

    def test_medium_message(self):
        self.run_and_wait(*_generate_unique_message(size=1000))

    def test_big_message(self):
        self.run_and_wait(*_generate_unique_message(size=90000))

    def test_multiline(self):
        sid, message = _generate_unique_message()
        self.run_and_wait(sid, message.replace(' ', '\n'))

    def test_send_header_application_type(self):
        sid, message = _generate_unique_message()
        headers = {'X-Application-Type': 'application-type-test'}
        response = self.run_and_wait(sid, message, headers)
        self.assertEqual('application-type-test', response[0]['_source']['application_type'])

    def test_send_header_dimensions(self):
        sid, message = _generate_unique_message()
        headers = {'X-Dimensions': 'server:WebServer01,environment:production'}
        response = self.run_and_wait(sid, message, headers)
        self.assertEqual('production', response[0]['_source']['environment'])
        self.assertEqual('WebServer01', response[0]['_source']['server'])


def _generate_unique_message(message=None, size=50):
    letters = string.ascii_lowercase

    def rand(size, space=True):
        space = ' ' if space else ''
        return ''.join((random.choice(letters+space) for letter in range(size)))

    sid = rand(10, space=False)
    if not message:
        message = rand(size)
    return sid, sid+' '+message
