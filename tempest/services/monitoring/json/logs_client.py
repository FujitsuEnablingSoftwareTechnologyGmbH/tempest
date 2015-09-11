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

import urllib
import time
import datetime
from tempest.common import service_client

from tempest import config
from oslo_serialization import jsonutils as json

CONF = config.CONF


class LogsClient(service_client.ServiceClient):

    version = '2.0'
    uri_prefix = "/v%s" % version

    def send_single_log(self, msg, headers=None):
        default_headers = {
            'X-Tenant-Id': 'b4265b0a48ae4fd3bdcee0ad8c2b6012',
            'X-Roles': 'admin'
        }
        default_headers.update(headers)
        uri = "/log/single"
        resp, body = self.post(self._uri(uri), msg, default_headers)
        self.expected_success(204, resp.status)
        return resp, body

    def _uri(self, url):
        return self.uri_prefix + url

class LogsSearchClientJSON(service_client.ServiceClient):

    uri_prefix = "/elasticsearch"

    def deserialize(self, body):
        return json.loads(body.replace("\n", ""))

    def serialize(self, body):
        return json.dumps(body)

    def get_metadata(self):
        uri = "/"

        response, body = self.get(self._uri(uri))
        self.expected_success(200, response.status)

        if body:
            body = self.deserialize(body)
        return response, body

    def count_search_messages(self, message):
        return len(self.search_messages(message))

    def search_messages(self, message):
        uri = '_search'
        body = self.serialize(dict(
            query=dict(
                term=dict(message=message)
            )
        ))
        response, body = self.post(self._uri(uri), body)
        self.expected_success(200, response.status)
        body = self.deserialize(body)
        return body.get('hits', {}).get('hits', [])

    def _uri(self, url):
        return '{}/{}'.format(self.uri_prefix, url)
