#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
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
# from tempest import exceptions
from tempest import test
import time
import json
import time


class MonitoringMetricTestJSON(base.BaseMonitoringTest):
    _interface = 'json'

    @classmethod
    def setUpClass(cls):
        super(MonitoringMetricTestJSON, cls).setUpClass()

    @test.attr(type="gate")
    def test_metric_list_by_name(self):
        # List metric by metric name
        m_name = 'cpu.idle_perc'
        body = self.monitoring_client.list_metric_by_name(m_name)
        response = json.loads(body.data)
        self.assertEquals(m_name, response['elements'][0]['name'])
        self.assertEqual('200', body.response['status'])

    @test.attr(type="gate")
    def test_create_metric_required_option(self):
        # Create a single metric with only required parameters
        count = 0
        m_name = "Test_Metric_1"
        m_value = 50.0
        body = self.monitoring_client.create_metric(name=m_name, value=m_value)
        self.assertEqual('204', body.response['status'])
        # Get metric
        params = {'name': m_name}
        while count < 30 :
            body = self.monitoring_client.list_metric(params)
            responseBody = json.loads(body.data)
            if len(responseBody['elements']) > 0:
                break
            time.sleep(2)
            count += 1
        self.assertGreater(len(responseBody['elements']), 0, "Metric is not listed.")
        self.assertEquals(m_name, responseBody['elements'][0]['name'])
        self.assertEqual('200', body.response['status'])

    @test.attr(type="gate")
    def test_create_metric_options(self):
        # Create a single metric with optional properties
        count = 0
        m_name = "Test_Metric_1"
        m_value = 1.0
        m_dimension = {
            "key1": "value1",
            "key2": "value2"
        }
        m_value_meta = {
            "key1": "value1",
            "key2": "value2"
        }
        m_timestamp = int(time.time() - 100) * 1000
        body = self.monitoring_client.create_metric(
            name=m_name, m_value=m_value, dimensions=m_dimension, timestamp=m_timestamp, value_meta=m_value_meta)
        self.assertEqual('204', body.response['status'])
        # Get metric
        params = {'name': m_name,'dimensions': 'key1:value1,key2:value2'}
        while count < 30 :
            body = self.monitoring_client.list_metric(params)
            responseBody = json.loads(body.data)
            if len(responseBody['elements']) > 0:
                break
            time.sleep(2)
            count += 1
        self.assertGreater(len(responseBody['elements']), 0, "Metric is not listed.")
        self.assertEquals(m_name, responseBody['elements'][0]['name'])
        self.assertEqual('200', body.response['status'])

    @test.attr(type="gate")
    def test_create_multiple_metric(self):
        # Create multiple metrics
        # m_name1 = data_utils.rand_name('metric')
        m_name1 = "Test_Metric_1"
        m_value1 = 1.0
        m_name2 = "Test_Metric_2"
        m_value2 = 1.0
        m_dimension2 = {
            'key1': 'value1',
            'key2': 'value2'
        }
        m_timestamp2 = int(time.time() - 100) * 1000
        body = self.monitoring_client.create_multiple_metric(name1=m_name1, m_value1=m_value1,
                                                             name2=m_name2, m_value2=m_value2, dimensions2=m_dimension2,
                                                             timestamp2=m_timestamp2)
        self.assertEqual('204', body.response['status'])

    @test.attr(type="gate")
    def test_metric_list(self):
        # List metric w/o parameters
        params = {}
        body = self.monitoring_client.list_metric(params)
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")

    @test.attr(type="gate")
    def test_list_metric_with_limit(self):
        # List metric with limit and offset
        # Get metric
        params = {'limit': '10'}
        body = self.monitoring_client.list_metric(params)
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")
        self.assertEqual('200', body.response['status'])

    @test.attr(type="gate")
    def test_list_metric_by_dimensions(self):
        # List metric with limit and offset
        # Get metric
        params = {'dimensions': 'service:monitoring'}
        body = self.monitoring_client.list_metric(params)
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")
        self.assertEqual('200', body.response['status'])


    @test.attr(type="gate")
    def test_list_metric_with_offset(self):
        # List metric with limit and offset
        # Get metric
        params = {'limit': '10'}
        body = self.monitoring_client.list_metric(params)
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")
        self.assertEqual('200', body.response['status'])
        offset = response['elements'][9]['id']
        params = {'offset': offset}
        body = self.monitoring_client.list_metric(params)
        response = json.loads(body.data)
        self.assertEqual('200', body.response['status'])
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")

    @test.attr(type="gate")
    def test_list_metric_with_offset_limit(self):
        # List metric with limit and offset
        # Get metric
        params = {'limit': '10'}
        body = self.monitoring_client.list_metric(params)
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")
        self.assertEqual('200', body.response['status'])
        offset = response['elements'][9]['id']
        params = {'limit': '10', 'offset': offset}
        body = self.monitoring_client.list_metric(params)
        response = json.loads(body.data)
        self.assertEqual('200', body.response['status'])
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")

    @test.attr(type="gate")
    def test_metric_names(self):
        # List metric names
        params = {}
        body = self.monitoring_client.list_metric_names(params)
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric names list is empty.")

    @test.attr(type="gate")
    def test_metric_names_by_dimensions(self):
        # List metric names by dimensions
        params = {'dimensions': 'service:monitoring'}
        body = self.monitoring_client.list_metric_names(params)
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric names list is empty.")

    # @test.attr(type="gate")
    # def test_metric_names_by_offset_limit(self):
    #     # List metric names with limit
    #     params = {'limit': '5'}
    #     body = self.monitoring_client.list_metric_names(params)
    #     self.assertEqual('200', body.response['status'])
    #     response = json.loads(body.data)
    #     self.assertGreater(len(response['elements']), 0, "Metric names list is empty.")
    #     offset_id = response['elements'][4]['id']
    #
    #     # List metric names with limit and offset
    #     params = {'limit': '10', 'offset' : offset_id}
    #     body = self.monitoring_client.list_metric_names(params)
    #     self.assertEqual('200', body.response['status'])
    #     response = json.loads(body.data)
    #     self.assertGreater(len(response['elements']), 0, "Metric names list is empty.")
    #
    #     # List metric names with offset
    #     params = {'offset' : offset_id}
    #     body = self.monitoring_client.list_metric_names(params)
    #     self.assertEqual('200', body.response['status'])
    #     response = json.loads(body.data)
    #     self.assertGreater(len(response['elements']), 0, "Metric names list is empty.")