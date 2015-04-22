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
from tempest_lib.common.utils import data_utils


class MonitoringNotificationTestJSON(base.BaseMonitoringTest):
    _interface = 'json'

    @classmethod
    def setUpClass(cls):
        super(MonitoringNotificationTestJSON, cls).setUpClass()

    @test.attr(type="gate")
    def test_create_notification(self):
        # Test case to check if new notification is created successfully.
        notification_name = data_utils.rand_name('notification-')
        notification_type = 'EMAIL'
        # Replace below email with valid email address as required.
        u_address = 'root@localhost'
        
        response = self.monitoring_client.create_notification(name=notification_name, type=notification_type, address=u_address)
        self.assertEqual(notification_name, response['name'])
        notification_id = response['id']
        # Delete notification
        self.monitoring_client.delete_notification(notification_id)

    @test.attr(type="gate")
    def test_get_notification(self):
        # Test case to check if getting notification is  successful.
        # Create notification first
        notification_name = data_utils.rand_name('notification-')
        notification_type = 'EMAIL'
        # Replace below email with valid email address as required.
        u_address = 'root@localhost'

        response = self.monitoring_client.create_notification(name=notification_name, type=notification_type, address=u_address)
        self.assertEqual(notification_name, response['name'])
        notification_id = response['id']
        # Get notification
        response = self.monitoring_client.get_notification(notification_id)
        self.assertIn(notification_name, response['name'])
        # Delete notification
        self.monitoring_client.delete_notification(notification_id)

    @test.attr(type="gate")
    def test_update_notification_name(self):
        # Test case to check if getting notification is  successful.
        # Create notification first
        notification_name = data_utils.rand_name('notification-')
        notification_type = 'EMAIL'
        # Replace below email with valid email address as required.
        u_address = 'root@localhost'

        response = self.monitoring_client.create_notification(name=notification_name, type=notification_type, address=u_address)
        self.assertEqual(notification_name, response['name'])
        notification_id = response['id']
        # Update notification
        new_name = notification_name + 'update'
        response = self.monitoring_client.update_notification_name(
                          notification_id, name=new_name, type=notification_type, address=u_address)
        self.assertIn(new_name, response['name'])
        # Delete notification
        self.monitoring_client.delete_notification(notification_id)

    @test.attr(type="gate")
    def test_update_notification_type(self):
        # Test case to check if getting notification is  successful.
        # Create notification first
        notification_name = data_utils.rand_name('notification-')
        notification_type = 'EMAIL'
        # Replace below email with valid email address as required.
        u_address = 'root@localhost'

        response = self.monitoring_client.create_notification(name=notification_name, type=notification_type, address=u_address)
        self.assertEqual(notification_name, response['name'])
        notification_id = response['id']
        # Update notification
        new_type = 'PAGERDUTY'
        response = self.monitoring_client.update_notification_type(
                          notification_id, type=new_type, name=notification_name, address=u_address)
        self.assertIn(new_type, response['type'])
        # Delete notification
        self.monitoring_client.delete_notification(notification_id)

    @test.attr(type="gate")
    def test_update_notification_address(self):
        # Test case to check if getting notification is  successful.
        # Create notification first
        notification_name = data_utils.rand_name('notification-')
        notification_type = 'EMAIL'
        # Replace below email with valid email address as required.
        u_address = 'root@localhost'

        response = self.monitoring_client.create_notification(name=notification_name, type=notification_type, address=u_address)
        self.assertEqual(notification_name, response['name'])
        notification_id = response['id']
        # Update notification
        new_address = 'test@test.com'
        response = self.monitoring_client.update_notification_address(
                          notification_id, address=new_address, name=notification_name, type=notification_type)
        self.assertIn(new_address, response['address'])
        # Delete notification
        self.monitoring_client.delete_notification(notification_id)

    @test.attr(type="gate")
    def test_notification_list(self):
        # List notifications
        params = {}
        body = self.monitoring_client.list_notifications(params)
        self.assertEqual('200', body.response['status'])

    @test.attr(type="gate")
    def test_notification_list_offset_limit(self):
        # List notifications
        params = {'limit': '100'}
        body = self.monitoring_client.list_notifications(params)
        self.assertEqual('200', body.response['status'])