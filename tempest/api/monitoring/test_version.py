#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.api.monitoring import base
from tempest import test
import json


class MonitoringVersionAPITestJSON(base.BaseMonitoringTest):
    _interface = 'json'
    # force_tenant_isolation = False

    @classmethod
    def resource_setup(cls):
        super(MonitoringVersionAPITestJSON, cls).resource_setup()

    @test.attr(type="gate")
    def test_monascaapi_version(self):
        # Get version
        resp = self.monitoring_client.get_version()
        self.assertEqual("v2.0", resp['id'])