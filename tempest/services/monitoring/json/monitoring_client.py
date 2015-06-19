# Copyright 2014 OpenStack Foundation
# All Rights Reserved.
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

import urllib
import time
import datetime
from tempest.common import service_client

from tempest import config
from oslo_serialization import jsonutils as json

CONF = config.CONF

class MonitoringClientJSON(service_client.ServiceClient):

    version = '2.0'
    uri_prefix = "v%s" % version


    def deserialize(self, body):
        return json.loads(body.replace("\n", ""))

    def serialize(self, body):
        return json.dumps(body)

    # def helper_list(self, uri, query=None, period=None):
    #     uri_dict = {}
    #     if query:
    #         uri_dict = {'q.field': query[0],
    #                     'q.op': query[1],
    #                     'q.value': query[2]}
    #     if period:
    #         uri_dict['period'] = period
    #     if uri_dict:
    #         uri += "?%s" % urllib.urlencode(uri_dict)
    #     resp, body = self.get(uri)
    #     self.expected_success(200, resp.status)
    #     body = self.deserialize(body)
    #     return service_client.ResponseBody(resp, body)

    def create_alarm_definition(self, **kwargs):
        uri = "/alarm-definitions/"
        body = self.serialize(kwargs)
        resp, body = self.post(uri, body)
        self.expected_success(201, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def list_alarm_definitions(self, params=None):
        url = '/alarm-definitions'
        url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        self.expected_success(200, resp.status)
        return service_client.ResponseBodyData(resp, body)

    def get_alarm_definition(self, alarm_def_id):
        uri = '/alarm-definitions/%s' % alarm_def_id
        resp, body = self.get(uri)
        self.expected_success(200, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def update_alarm_definition(self, alarm_def_id, **kwargs):
        uri = "/alarm-definitions/%s" % alarm_def_id
        body = self.serialize(kwargs)
        resp, body = self.put(uri, body)
        self.expected_success(200, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def patch_alarm_definition(self, alarm_def_id, **kwargs):
        uri = "/alarm-definitions/%s" % alarm_def_id
        body = self.serialize(kwargs)
        resp, body = self.patch(uri, body)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def delete_alarm_definition(self, alarm_def_id):
        uri = "/alarm-definitions/%s" % alarm_def_id
        resp, body = self.delete(uri)
        if body:
            body = self.deserialize(body)
        self.expected_success(204, resp.status)
        return service_client.ResponseBody(resp, body)

    def list_alarms(self, **kwargs):
        uri = '/alarms'
        m_alarm_definition_id = kwargs.get('alarm_definition_id', None)
        m_metric_name = kwargs.get('metric_name', None)
        m_metric_dimensions = kwargs.get('metric_dimensions', None)
        m_state = kwargs.get('state', None)
        m_state_updated_start_time = kwargs.get('state_updated_start_time', None)
        m_offset = kwargs.get('offset', None)
        m_limit = kwargs.get('limit', None)
        if m_alarm_definition_id is not None:
            uri += '?alarm_definition_id=' + m_alarm_definition_id
        if m_metric_name is not None:
            uri += '?metric_name=' + m_metric_name
        if m_metric_dimensions is not None:
            uri += '?metric_dimensions=' + m_metric_dimensions
        if m_state is not None:
            uri += '?state=' + m_state
        if m_state_updated_start_time is not None:
            uri += '?state_updated_start_time=' + m_state_updated_start_time
        if m_offset is not None:
            uri += '?offset=' + m_offset
        if m_limit is not None:
            uri += '?limit=' + m_limit

        resp, body = self.get(uri)
        self.expected_success(200, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def get_alarm(self, alarm_id):
        uri = '/alarms/%s' % alarm_id
        resp, body = self.get(uri)
        self.expected_success(200, resp.status)
        if body:
            body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def update_alarm(self, alarm_id, **kwargs):
        uri = "/alarms/%s" % alarm_id
        body = self.serialize(kwargs)
        resp, body = self.put(uri, body)
        self.expected_success(200, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def patch_alarm(self, alarm_id, **kwargs):
        uri = "/alarms/%s" % alarm_id
        body = self.serialize(kwargs)
        resp, body = self.patch(uri, body)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def delete_alarm(self, alarm_id):
        uri = "/alarms/%s" % alarm_id
        resp, body = self.delete(uri)
        if body:
            body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def get_alarms_by_def_id(self, alarm_def_id):
        uri = '/alarms?alarm_definition_id=' + alarm_def_id
        resp, body = self.get(uri)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)


    def get_alarms_by_metric_name(self, metric_name):
        uri = '/alarms?metric_name=' + metric_name
        resp, body = self.get(uri)
        self.expected_success(200, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def get_alarms_by_metric_dimensions(self, metric_name, metric_dimensions):
        uri = '/alarms?metric_name=' + metric_name + '&metric_dimensions=' + metric_dimensions
        resp, body = self.get(uri)
        self.expected_success(200, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def get_alarms_by_state(self, alarm_def_id, state):
        uri = '/alarms?alarm_definition_id=' + alarm_def_id + '&state=' + state
        resp, body = self.get(uri)
        self.expected_success(200, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def get_alarms_state_history_by_dimensions(self, metric_dimensions):
        uri = '/alarms/state-history?dimensions=' + metric_dimensions
        resp, body = self.get(uri)
        self.expected_success(200, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def get_alarms_state_history_by_dimensions_and_time(self, **kwargs):
        uri = '/alarms/state-history'
        default_starttime = (datetime.datetime.now() - datetime.timedelta(minutes=2880)).strftime('%Y-%m-%d %H:%M:%S')
        default_starttime = default_starttime.replace(' ', 'T') + 'Z'
        m_dimension = kwargs.get('dimensions', None)
        m_start_time = kwargs.get('start_time', default_starttime)
        m_end_time = kwargs.get('end_time', None)
        if m_dimension is not None:
            uri += '?dimensions=' + m_dimension
        uri += '&start_time=' + m_start_time
        if m_end_time is not None:
            uri += '&end_time=' + m_end_time
        resp, body = self.get(uri)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def get_alarm_state_history_by_alarm_id(self, alarm_id):
        uri = "/alarms/%s/state-history" % alarm_id
        resp, body = self.get(uri)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def list_notifications(self, params=None):
        url = '/notification-methods'
        url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        self.expected_success(200, resp.status)
        return service_client.ResponseBodyData(resp, body)

    def create_notification(self, **kwargs):
        """Create a notification."""
        uri = '/notification-methods'
        body = self.serialize(kwargs)
        resp, body = self.post(uri, body)
        self.expected_success(201, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def delete_notification(self, notification_id):
        """Delete a notification."""
        uri = '/notification-methods/' + notification_id
        resp, body = self.delete(uri)
        if body:
            body = self.deserialize(body)
        self.expected_success(204, resp.status)
        return service_client.ResponseBody(resp, body)

    def get_notification(self, notification_id):
        """Get specific notification"""
        uri = '/notification-methods/' + notification_id
        resp, body = self.get(uri)
        self.expected_success(200, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def update_notification_name(self, notification_id, **kwargs):
        """Update a notification."""
        url = '/notification-methods/' + notification_id
        body = self.serialize(kwargs)
        # notification_type = kwargs.get('type', None)
        # address = kwargs.get('address', None)
        # post_body = {
        #     'name': notification_name,
        #     'type': notification_type,
        #     'address': address
        # }
        # post_body = json.dumps(post_body)
        resp, body = self.put(url, body)
        self.expected_success(200, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def update_notification_type(self, notification_id, **kwargs):
        """Update a notification."""
        url = '/notification-methods/' + notification_id
        body = self.serialize(kwargs)
        resp, body = self.put(url, body)
        self.expected_success(200, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def update_notification_address(self, notification_id, **kwargs):
        """Update a notification."""
        url = '/notification-methods/' + notification_id
        body = self.serialize(kwargs)
        resp, body = self.put(url, body)
        self.expected_success(200, resp.status)
        body = self.deserialize(body)
        return service_client.ResponseBody(resp, body)

    def list_metric_no_option(self):
        """List metric w/o options."""
        url = '/metrics'
        resp, body = self.get(url)
        self.expected_success(200, resp.status)
        return service_client.ResponseBodyData(resp, body)

    def list_metric_by_name(self, metric_name):
        """List metric w/o options."""
        url = '/metrics?name=' + metric_name
        resp, body = self.get(url)
        self.expected_success(200, resp.status)
        return service_client.ResponseBodyData(resp, body)

    def list_metric_names(self, params=None):
        """List metric."""
        url = '/metrics/names'
        url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        self.expected_success(200, resp.status)
        return service_client.ResponseBodyData(resp, body)



    def list_metric(self, params=None):
        """List metric."""
        url = '/metrics'
        # m_name = kwargs.get('name', None)
        # m_dimension = kwargs.get('dimensions', None)
        # m_limit = kwargs.get('limit', None)
        # m_offset = kwargs.get('offset', None)
        # if m_name is not None:
        #    url  += '?name=' + m_name
        # if m_dimension is not None:
        #    keylist = m_dimension.keys()
        #    dimension = ''
        #    for index, key in enumerate(keylist):
        #        dimension += key + ':' + str(m_dimension.get(key))
        #        if index < len(keylist)-1:
        #            dimension += ','
        #    url += '&dimensions=' + dimension
        # if m_limit is not None:
        #     url += '&limit=' + str(m_limit)
        # if m_offset is not None:
        #     url += '&offset=' + str(m_offset)
        url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        self.expected_success(200, resp.status)
        return service_client.ResponseBodyData(resp, body)


    def create_metric(self, **kwargs):
        """Create a metric."""
        url = '/metrics'
        m_name = kwargs.get('name', None)
        m_value = kwargs.get('value', None)
        m_dimension = kwargs.get('dimensions', None)
        m_timestamp = kwargs.get('timestamp', int(time.time()*1000))
        m_value_meta = kwargs.get('value_meta', None)
        post_body = {
            'name': m_name,
            'value': m_value,
            'dimensions': m_dimension,
            'timestamp': m_timestamp,
            'value_meta': m_value_meta
        }
        post_body = json.dumps(post_body)
        resp, body = self.post(url, post_body)
        return service_client.ResponseBody(resp, body)

    def create_multiple_metric(self, **kwargs):
        """Create a metric."""
        url = '/metrics'
        m_name1 = kwargs.get('name1', None)
        m_value1 = kwargs.get('value1', None)
        m_dimension1 = kwargs.get('dimensions1', None)
        m_value_meta1 = kwargs.get('value_meta', None)
        m_timestamp1 = kwargs.get('timestamp1', int(time.time()*1000))

        post_body1 = {
            'name': m_name1,
            'value': m_value1,
            'dimensions': m_dimension1,
            'timestamp': m_timestamp1,
            'value_meta': m_value_meta1
        }
        post_body1 = json.dumps(post_body1)
        m_name2 = kwargs.get('name2', None)
        m_value2 = kwargs.get('value2', None)
        m_dimension2 = kwargs.get('dimensions2', None)
        m_value_meta2 = kwargs.get('value_meta', None)
        m_timestamp2 = kwargs.get('timestamp2', int(time.time()*1000))
        post_body2 = {
            'name': m_name2,
            'value': m_value2,
            'dimensions': m_dimension2,
            'timestamp': m_timestamp2,
            'value_meta': m_value_meta2
        }
        post_body2 = json.dumps(post_body2)
        m_array = '[' + post_body1 + ',' + post_body2 + ']'
        resp, body = self.post(url, m_array)
        return service_client.ResponseBody(resp, body)

    def get_version(self, params=None):
        """List monasca api version."""
        url = '/'
        url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        self.expected_success(200, resp.status)
        return service_client.ResponseBodyData(resp, body)

    def metric_measurement(self, **kwargs):
        """List a metric measurement."""
        url = '/metrics/measurements'
        default_starttime = (datetime.datetime.now() - datetime.timedelta(minutes=2880)).strftime('%Y-%m-%d %H:%M:%S')
        default_starttime = default_starttime.replace(' ', 'T') + 'Z'
        m_name = kwargs.get('name', None)
        m_dimension = kwargs.get('dimensions', None)
        m_start_time = kwargs.get('start_time', default_starttime)
        m_end_time = kwargs.get('end_time', None)
        m_period = kwargs.get('period', None)
        m_limit = kwargs.get('limit', None)
        m_offset = kwargs.get('offset', None)
        m_merge_metrics = kwargs.get('merge_metrics', None)
        url += '?start_time=' + m_start_time
        if m_name is not None:
            url += '&name=' + m_name
        if m_dimension is not None:
            keylist = m_dimension.keys()
            dimension = ''
            for index, key in enumerate(keylist):
                dimension += key + ':' + str(m_dimension.get(key))
                if index < len(keylist)-1:
                    dimension += ','
            url += '&dimensions=' + dimension
        if m_end_time is not None:
            url += '&end_time=' + m_end_time
        if m_period is not None:
            url += '&period=' + str(m_period)
        if m_offset is not None:
            url += '&offset=' + m_offset
        if m_limit is not None:
            url += '&limit=' + m_limit
        if m_merge_metrics is not None:
            url += '&merge_metrics=' + m_merge_metrics
        resp, body = self.get(url)
        return service_client.ResponseBodyData(resp, body)

    def metric_statistics(self, **kwargs):
        """List a metric statistics."""
        url = '/metrics/statistics'
        default_starttime = (datetime.datetime.now() - datetime.timedelta(minutes=2880)).strftime('%Y-%m-%d %H:%M:%S')
        default_starttime = default_starttime.replace(' ', 'T') + 'Z'
        m_name = kwargs.get('name', None)
        m_dimension = kwargs.get('dimensions', None)
        m_start_time = kwargs.get('start_time', default_starttime)
        m_end_time = kwargs.get('end_time', None)
        m_statistics = kwargs.get('statistics', None)
        m_period = kwargs.get('period', 300)
        m_offset = kwargs.get('offset', None)
        m_limit = kwargs.get('limit', None)
        m_merge_metrics = kwargs.get('merge_metrics', None)
        url += '?name=' + m_name + '&statistics=' + m_statistics + '&start_time=' + m_start_time
        if m_dimension is not None:
            # keylist = m_dimension.keys()
            # dimension = ''
            # for index, key in enumerate(keylist):
            #     dimension += key + ':' + str(m_dimension.get(key))
            #     if index < len(keylist)-1:
            #         dimension += ','
            url += '&dimensions=' + m_dimension
        if m_end_time is not None:
            url += '&end_time=' + m_end_time
        if m_offset is not None:
            url += '&offset=' + m_offset
        if m_limit is not None:
            url += '&limit=' + m_limit
        if m_period is not None:
            url += '&period=' + str(m_period)
        if m_merge_metrics is not None:
            url += '&merge_metrics=' + m_merge_metrics
        resp, body = self.get(url)
        return service_client.ResponseBodyData(resp, body)


