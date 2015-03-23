#
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
from tempest_lib import exceptions as lib_exc
from tempest import test
from tempest_lib.common.utils import data_utils
import datetime

class MonitoringMetricTestJSON(base.BaseMonitoringTest):
    _interface = 'json'

    @classmethod
    def setUpClass(cls):
        super(MonitoringMetricTestJSON, cls).setUpClass()

    @test.attr(type="gate")
    def test_metric_statistics_required_option(self):
        # Create a single metric with only required parameters
        m_name = "Test_Metric_1"
        m_value = 1.0 
        body = self.monitoring_client.create_metric(name=m_name, value=m_value)
        self.assertEqual('204', body.response['status'])
        # Get metric statistics
        m_statistics = 'AVG'
        body = self.monitoring_client.metric_statistics(name=m_name,statistics=m_statistics)
        self.assertEqual('200', body.response['status'])

    @test.attr(type="gate")
    def test_create_metric_options(self):
        # Create a single metric with optional 
        m_name = "Test_Metric_1"
        m_value = 1.0
        m_dimension = {
                      'key1': 'value1',
                      'key2': 'value2'
                      }
        body = self.monitoring_client.create_metric(
                     name=m_name, m_value=m_value, dimensions=m_dimension)
        self.assertEqual('204', body.response['status'])
        # Get metric statics
        m_statistics = 'avg,min,max,count,sum'
        m_endtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        m_endtime = m_endtime.replace(' ', 'T') + 'Z'
        body = self.monitoring_client.list_metric(name=m_name, dimensions=m_dimension,
                     statistics=m_statistics, end_time=m_endtime)
        self.assertEqual('200', body.response['status'])
