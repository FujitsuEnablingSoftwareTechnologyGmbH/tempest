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
from tempest_lib.common.utils import data_utils
from tempest_lib import exceptions as lib_exc
from tempest import test
import datetime
import time
import json

class MonitoringMeasurementAPITestJSON(base.BaseMonitoringTest):
    _interface = 'json'

    @classmethod
    def setUpClass(cls):
        super(MonitoringMeasurementAPITestJSON, cls).setUpClass()

    @test.attr(type="gate")
    def test_measurement_with_metric_name(self):
        # List metric measurement with metric name
        metric_name="cpu.idle_perc"
        body = self.monitoring_client.metric_measurement(name=metric_name, merge_metrics="true")
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)

    @test.attr(type="gate")
    def test_measurement_metric_name_and_dimensions(self):
        # Get metric measurement with metric name and dimensions
        metric_name = 'cpu.user_perc'
        metric_dimension = {'service': 'monitoring'}
        body = self.monitoring_client.metric_measurement(name=metric_name, dimensions=metric_dimension, merge_metrics="true")
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)

    @test.attr(type="gate")
    def test_measurement_with_limit_and_end_time(self):
        # List metric measurement with metric name, limit and end time
        metric_name = 'cpu.idle_perc'
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_time = current_time.replace(' ', 'T') + 'Z'
        m_limit = 5
        body = self.monitoring_client.metric_measurement(name=metric_name, end_time=current_time, limit=str(m_limit),
                                                         merge_metrics="true")
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)

    @test.attr(type="gate")
    def test_custom_metric_measurement_dimension(self):
        # List metric measurement with custom metric name and dimension
        # Create metric with dimension
        m_name = "Test_Metric_1"
        m_value = 1.0
        m_dimension = {
                      'key1': 'value1',
                      'key2': 'value2'
                      }
        m_timestamp = int(time.time() - 100)*1000
        body = self.monitoring_client.create_metric(
                     name=m_name, m_value=m_value, dimensions=m_dimension,timestamp=m_timestamp)
        self.assertEqual('204', body.response['status'])
        # List measurement
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_time = current_time.replace(' ', 'T') + 'Z'
        body = self.monitoring_client.metric_measurement(name=m_name, dimensions=m_dimension,
                     end_time=current_time)
        self.assertEqual('200', body.response['status'])