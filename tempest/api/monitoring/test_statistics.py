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
import json

class MonitoringMetricTestJSON(base.BaseMonitoringTest):
    _interface = 'json'

    @classmethod
    def setUpClass(cls):
        super(MonitoringMetricTestJSON, cls).setUpClass()

    @test.attr(type="gate")
    def test_list_metric_statistics_average(self):
        # Create a single metric with only required parameters
        metric_name = "cpu.idle_perc"
        # Get metric statistics
        m_statistics = 'avg'
        body = self.monitoring_client.metric_statistics(name=metric_name, statistics=m_statistics, merge_metrics="true")
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")
        self.assertEqual(metric_name, response['elements'][0]['name'], "Metric name not listed")
        self.assertIn('avg', str(response), "average column is not displayed")

    @test.attr(type="gate")
    def test_list_metric_statistics_options(self):
        # Metric statistics with start time and end time
        metric_name = "cpu.idle_perc"
        # Get metric statics
        m_statistics = 'avg,min,max,count,sum'
        m_endtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        m_endtime = m_endtime.replace(' ', 'T') + 'Z'
        body = self.monitoring_client.metric_statistics(name=metric_name, dimensions='service:monitoring',
                     statistics=m_statistics, end_time=m_endtime, merge_metrics='true')
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")
        self.assertEqual(metric_name, response['elements'][0]['name'], "Metric name not listed")

    @test.attr(type="gate")
    def test_list_metric_statistics_sum_with_limit_offset(self):
        # Metric statistics sum with limit
        metric_name = "cpu.idle_perc"
        # Get metric statics
        m_statistics = 'sum'
        m_endtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        m_endtime = m_endtime.replace(' ', 'T') + 'Z'
        body = self.monitoring_client.metric_statistics(name=metric_name, dimensions='service:monitoring',
                     statistics=m_statistics, end_time=m_endtime, merge_metrics='true', limit='10')
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")
        self.assertEqual(metric_name, response['elements'][0]['name'], "Metric name not listed")
        offset_id = response['elements'][0]['statistics'][9][0]

        # Metric statistics with limit and offset
        body = self.monitoring_client.metric_statistics(name=metric_name, dimensions='service:monitoring',
                     statistics=m_statistics, end_time=m_endtime, merge_metrics='true', limit='10', offset=offset_id)
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")
        self.assertEqual(metric_name, response['elements'][0]['name'], "Metric name not listed")

    @test.attr(type="gate")
    def test_list_metric_statistics_min(self):
        # Metric statistics with min
        metric_name = "cpu.idle_perc"
        # Get metric statistics
        m_statistics = 'min'
        body = self.monitoring_client.metric_statistics(name=metric_name, statistics=m_statistics, merge_metrics="true")
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")
        self.assertEqual(metric_name, response['elements'][0]['name'], "Metric name not listed")
        self.assertIn('min', str(response), "min column is not displayed")

    @test.attr(type="gate")
    def test_list_metric_statistics_max(self):
        # Metric statistics with max
        metric_name = "cpu.idle_perc"
        # Get metric statistics
        m_statistics = 'max'
        body = self.monitoring_client.metric_statistics(name=metric_name, statistics=m_statistics, merge_metrics="true")
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")
        self.assertEqual(metric_name, response['elements'][0]['name'], "Metric name not listed")
        self.assertIn('max', str(response), "max column is not displayed")

    @test.attr(type="gate")
    def test_list_metric_statistics_count(self):
        # Metric statistics with count
        metric_name = "cpu.idle_perc"
        # Get metric statistics
        m_statistics = 'count'
        body = self.monitoring_client.metric_statistics(name=metric_name, statistics=m_statistics, merge_metrics="true")
        self.assertEqual('200', body.response['status'])
        response = json.loads(body.data)
        self.assertGreater(len(response['elements']), 0, "Metric list is empty.")
        self.assertEqual(metric_name, response['elements'][0]['name'], "Metric name not listed")
        self.assertIn('count', str(response), "count column is not displayed")