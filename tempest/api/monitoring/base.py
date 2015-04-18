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

import time

from tempest_lib.common.utils import data_utils
from tempest_lib import exceptions as lib_exc

from tempest import clients
from tempest import config
from tempest import exceptions
from tempest_lib.common.rest_client import logging

from oslo_utils import timeutils
import tempest.test

CONF = config.CONF

LOG = logging.getLogger(__name__)


class BaseMonitoringTest(tempest.test.BaseTestCase):

    """Base test case class for all Monitoring API tests."""

    @classmethod
    def resource_setup(cls):
        if not CONF.service_available.monasca:
             raise cls.skipException("Monasca support is required")
        super(BaseMonitoringTest, cls).resource_setup()
        cls._interface = 'json'
        cls.os = clients.Manager()

        cls.monitoring_client = cls.os.monitoring_client
        cls.alarm_def_ids = []


    @classmethod
    def create_alarm_definition(cls, **kwargs):
        body = cls.monitoring_client.create_alarm_definition(
            name=data_utils.rand_name('monitoring_alarm_definitions'),
            **kwargs)
        cls.alarm_def_ids.append(body['id'])
        return body

    @classmethod
    def create_server(cls):
        resp, body = cls.servers_client.create_server(
            data_utils.rand_name('monasca-instance'),
            CONF.compute.image_ref, CONF.compute.flavor_ref,
            wait_until='ACTIVE')
        cls.server_ids.append(body['id'])
        return resp, body

    @classmethod
    def create_image(cls, client):
        resp, body = client.create_image(
            data_utils.rand_name('image'), container_format='bare',
            disk_format='raw', visibility='private')
        cls.image_ids.append(body['id'])
        return resp, body

    @staticmethod
    def cleanup_resources(method, list_of_ids):
        for resource_id in list_of_ids:
            try:
                method(resource_id)
            except lib_exc.NotFound:
                pass

    @classmethod
    def resource_cleanup(cls):
        cls.cleanup_resources(cls.monitoring_client.delete_alarm_definition, cls.alarm_def_ids)
        super(BaseMonitoringTest, cls).resource_cleanup()

    def await_samples(self, metric, query):
        """
        This method is to wait for sample to add it to database.
        There are long time delays when using Postgresql (or Mysql)
        database as monasca backend
        """
        timeout = CONF.compute.build_timeout
        start = timeutils.utcnow()
        while timeutils.delta_seconds(start, timeutils.utcnow()) < timeout:
            resp, body = self.monitoring_client.list_samples(metric, query)
            self.assertEqual(resp.status, 200)
            if body:
                return resp, body
            time.sleep(CONF.compute.build_interval)

        raise exceptions.TimeoutException(
            'Sample for metric:%s with query:%s has not been added to the '
            'database within %d seconds' % (metric, query,
                                            CONF.compute.build_timeout))
