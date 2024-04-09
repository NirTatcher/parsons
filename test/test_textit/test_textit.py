import unittest
import requests_mock
from parsons.textit.textit import TextIt
from parsons import Table


class TestTextIt(unittest.TestCase):

    def setUp(self):

        self.textit = TextIt("TEXTIT_API_KEY")

    def tearDown(self):

        pass

    @requests_mock.Mocker()
    def test_get_archives(self, m):
        # Mock the API response
        api_response = {
            "next": None,
            "previous": None,
            "count": 248,
            "results": [
                {
                    "archive_type": "message",
                    "start_date": "2017-02-20",
                    "period": "daily",
                    "record_count": 1432,
                    "size": 2304,
                    "hash": "feca9988b7772c003204a28bd741d0d0",
                    "download_url": "<redacted>"
                }
            ]
        }
        m.get('https://textit.in/api/v2/archives.json', json=api_response)

        # Instantiate the TextIt connector
     

        # Call the get_archives function
        result = self.textit.get_archives()

        result_data_dicts = result.to_dicts()
        expected_data_dicts = api_response['results']

        # Assert the result matches the expected output
        self.assertEqual(result_data_dicts,expected_data_dicts)

    @requests_mock.Mocker()

    def test_get_boundaries(self, m):
        # Mock the API response
        api_response = {
            "next": None,
            "previous": None,
            "results": [
                {
                    "osm_id": "1708283",
                    "name": "Kigali City",
                    "parent": {"osm_id": "171496", "name": "Rwanda"},
                    "level": 1,
                    "aliases": ["Kigari"],
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [
                                [
                                    [7.5251021, 5.0504713],
                                    [7.5330272, 5.0423498]
                                ]
                            ]
                        ]
                    }
                }
            ]
        }
        m.get('https://textit.in/api/v2/boundaries.json', json=api_response)


        # Call the get_boundaries function without geometry
        result_without_geometry = self.textit.get_boundaries()
        result_without_geometry_dicts = result_without_geometry.to_dicts()
        expected_without_geometry = api_response['results']
        self.assertEqual(result_without_geometry_dicts, expected_without_geometry)

        # Call the get_boundaries function with geometry
        result_with_geometry = self.textit.get_boundaries(geometry=True)
        result_with_geometry_dicts = result_with_geometry.to_dicts()
        expected_with_geometry_dicts = api_response['results']

        # Assert the result matches the expected output
        self.assertEqual(result_with_geometry_dicts, expected_with_geometry_dicts)
       


    @requests_mock.Mocker()
    def test_list_broadcasts(self, m):
        # Mock the API response
        api_response = {
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 12345,
                    "status": "sent",
                    "text": {"eng": "Hello, World!"},
                    "created_on": "2021-01-01T12:00:00.000Z"
                }
            ]
        }
        m.get('https://textit.in/api/v2/broadcasts.json', json=api_response)

        # Call the list_broadcasts function
        result = self.textit.list_broadcasts()

        # Convert result to list of dicts for comparison
        result_data_dicts = result.to_dicts()
        expected_data_dicts = api_response['results']

        # Assert the result matches the expected output
        self.assertEqual(expected_data_dicts, result_data_dicts)

    @requests_mock.Mocker()
    def test_send_broadcasts(self, m):
        # Mock the API response for sending a broadcast
        api_response = {
            "id": 12345,
            "status": "sent",
            "text": {"eng": "Hello, World!"},
            "created_on": "2021-01-01T12:00:00.000Z"
        }
        m.post('https://textit.in/api/v2/broadcasts.json', json=api_response, status_code=201)

        # Define payload for sending a broadcast
        payload = {
            "urns": ["tel:+1234567890"],
            "text": {"eng": "Hello, World!"}
        }

        # Call the send_broadcast function
        result = self.textit.send_broadcast(**payload)

        # Assert the result matches the expected output
        self.assertEqual(api_response, result)


    @requests_mock.Mocker()
    def test_list_all_campaigns(self, m):
        # Mock the API response for listing all campaigns
        api_response = {
            "next": None,
            "previous": None,
            "results": [
                {
                    "uuid": "f14e4ff0-724d-43fe-a953-1d16aefd1c00",
                    "name": "Reminders",
                    "archived": False,
                    "group": {"uuid": "7ae473e8-f1b5-4998-bd9c-eb8e28c92fa9", "name": "Reporters"},
                    "created_on": "2013-08-19T19:11:21.088Z"
                }
            ]
        }
        m.get('https://textit.in/api/v2/campaigns.json', json=api_response)

        # Call the list_all_campaigns function
        result = self.textit.list_all_campaigns()

        # Convert result to list of dicts for comparison
        result_data_dicts = result.to_dicts()
        expected_data_dicts = api_response['results']

        # Assert the result matches the expected output
        self.assertEqual(expected_data_dicts, result_data_dicts)


    @requests_mock.Mocker()
    def test_add_campaign(self, m):
        # Mock the API response for adding a campaign
        api_response = {
            "uuid": "f14e4ff0-724d-43fe-a953-1d16aefd1c00",
            "name": "Reminders",
            "archived": False,
            "group": {"uuid": "7ae473e8-f1b5-4998-bd9c-eb8e28c92fa9", "name": "Reporters"},
            "created_on": "2013-08-19T19:11:21.088Z"
        }
        m.post('https://textit.in/api/v2/campaigns.json', json=api_response, status_code=201)

        # Define payload for adding a campaign
        payload = {
            "name": "Reminders",
            "group_uuid": "7ae473e8-f1b5-4998-bd9c-eb8e28c92fa9"
        }

        # Call the add_campaign function
        result = self.textit.add_campaign(**payload)

        # Assert the result matches the expected output
        self.assertEqual(api_response, result)
    
    @requests_mock.Mocker()
    def test_update_campaign(self, m):
        # Mock the API response for updating a campaign
        api_response = {
            "uuid": "f14e4ff0-724d-43fe-a953-1d16aefd1c00",
            "name": "Reminders II",
            "archived": False,
            "group": {"uuid": "7ae473e8-f1b5-4998-bd9c-eb8e28c92fa9", "name": "Reporters"},
            "created_on": "2013-08-19T19:11:21.088Z"
        }
        m.post('https://textit.in/api/v2/campaigns.json?uuid=f14e4ff0-724d-43fe-a953-1d16aefd1c00', json=api_response)

        # Define payload for updating a campaign
        payload = {
            "uuid": "f14e4ff0-724d-43fe-a953-1d16aefd1c00",
            "name": "Reminders II",
            "group_uuid": "7ae473e8-f1b5-4998-bd9c-eb8e28c92fa9"
        }

        # Call the update_campaign function
        result = self.textit.update_campaign(**payload)

        # Assert the result matches the expected output
        self.assertEqual(api_response, result)

    @requests_mock.Mocker()
    def test_list_all_campaign_events(self, m):
        # Mock the API response for listing all campaign events
        api_response = {
            "next": None,
            "previous": None,
                "results": [
                    {
                        "uuid": "f14e4ff0-724d-43fe-a953-1d16aefd1c00",
                        "campaign": {"uuid": "f14e4ff0-724d-43fe-a953-1d16aefd1c00", "name": "Reminders"},
                        "relative_to": {"key": "registration", "name": "Registration Date"},
                        "offset": 7,
                        "unit": "days",
                        "delivery_hour": 9,
                        "flow": {"uuid": "09d23a05-47fe-11e4-bfe9-b8f6b119e9ab", "name": "Survey"},
                        "message": None,
                        "created_on": "2013-08-19T19:11:21.088Z"
                    },
                    
            ]
        }
        m.get('https://textit.in/api/v2/campaign_events.json', json=api_response)

        # Call the list_all_campaign_events function
        result = self.textit.list_all_campaign_events()

        # Convert result to list of dicts for comparison
        result_data_dicts = result.to_dicts()
        expected_data_dicts = api_response['results']

        # Assert the result matches the expected output
        self.assertEqual(expected_data_dicts, result_data_dicts)


    @requests_mock.Mocker()
    def test_add_campaign_event(self, m):
        # Mock the API response for adding a campaign event
        api_response = {
            "campaign": "f14e4ff0-724d-43fe-a953-1d16aefd1c00",
            "relative_to": "last_hit",
            "offset": 160,
            "unit": "weeks",
            "delivery_hour": -1,
            "message": "Feeling sick and helpless, lost the compass where self is."
        }
        m.post('https://textit.in/api/v2/campaign_events.json', json=api_response, status_code=201)

        # Define payload for adding a campaign event
        payload = {
            "campaign": "f14e4ff0-724d-43fe-a953-1d16aefd1c00",
            "relative_to": "last_hit",
            "offset": 160,
            "unit": "weeks",
            "delivery_hour": -1,
            "message": "Feeling sick and helpless, lost the compass where self is."
        }

        # Call the add_campaign_event function
        result = self.textit.add_campaign_event(**payload)

        # Assert the result matches the expected output
        self.assertEqual(api_response, result)


    @requests_mock.Mocker()
    def test_update_campaign_event(self, m):
        # Mock the API response for updating a campaign event
        api_response = {
                "relative_to": "last_hit",
                "offset": 100,
                "unit": "weeks",
                "delivery_hour": -1,
                "message": "Feeling sick and helpless, lost the compass where self is."
        }
        m.post('https://textit.in/api/v2/campaign_events.json?uuid=6a6d7531-6b44-4c45-8c33-957ddd8dfabc', json=api_response)

        # Define payload for updating a campaign event
        payload = {
                "uuid":"6a6d7531-6b44-4c45-8c33-957ddd8dfabc",
                "relative_to": "last_hit",
                "offset": 100,

                "unit": "weeks",
                "delivery_hour": -1,
                "message": "Feeling sick and helpless, lost the compass where self is."
        }

        # Call the update_campaign_event function
        result = self.textit.update_campaign_event(**payload)

        # Assert the result matches the expected output
        self.assertEqual(api_response, result)

    @requests_mock.Mocker()
    def test_delete_campaign_event(self, m):
        # Mock the API response for deleting a campaign event
        m.delete('https://textit.in/api/v2/campaign_events.json?uuid=6a6d7531-6b44-4c45-8c33-957ddd8dfabc', status_code=204)

        # Call the delete_campaign_event function with the UUID of the event to delete
        response = self.textit.delete_campaign_event("6a6d7531-6b44-4c45-8c33-957ddd8dfabc")

        # Assert the response status code matches the expected output (204)
        self.assertEqual(response, 204)
    
    @requests_mock.Mocker()
    def test_list_all_channels(self, m):
        # Mock the API response for listing all channels
        api_response = {
            "next": None,
            "previous": None,
            "results": [
                        {
                    "uuid": "09d23a05-47fe-11e4-bfe9-b8f6b119e9ab",
                    "name": "Android Phone",
                    "address": "+250788123123",
                    "country": "RW",
                    "device": {
                        "name": "Nexus 5X",
                        "power_level": 99,
                        "power_status": "STATUS_DISCHARGING",
                        "power_source": "BATTERY",
                        "network_type": "WIFI",
                    },
                    "last_seen": "2016-03-01T05:31:27.456",
                    "created_on": "2014-06-23T09:34:12.866",
                }
            ]
        }
        m.get('https://textit.in/api/v2/channels.json', json=api_response)

        # Call the list_all_channels function
        result = self.textit.list_all_channels()

        # Convert result to list of dicts for comparison
        result_data_dicts = result.to_dicts()
        expected_data_dicts = api_response['results']

        # Assert the result matches the expected output
        self.assertEqual(expected_data_dicts, result_data_dicts)
        

    @requests_mock.Mocker()
    def test_list_all_channel_events(self, m):
        # Mock the API response for listing all channel events
        api_response = {
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 4,
                    "channel": {"uuid": "9a8b001e-a913-486c-80f4-1356e23f582e", "name": "Vonage"},
                    "type": "call-in",
                    "contact": {"uuid": "d33e9ad5-5c35-414c-abd4-e7451c69ff1d", "name": "Bob McFlow"},
                    "extra": {"duration": 606},
                    "occurred_on": "2013-02-27T09:06:12.123",
                    "created_on": "2013-02-27T09:06:15.456"
                }
            ]
        }
        m.get('https://textit.in/api/v2/channel_events.json', json=api_response)


        result = self.textit.list_all_channel_events()
       
        # Assert the result matches the expected output
        expected_data_dicts = api_response['results']
        self.assertEqual(expected_data_dicts, result)

    @requests_mock.Mocker()
    def test_list_all_classifiers_with_uuid(self, m):
        # Mock the API response for listing a specific classifier by UUID
        api_response = {
            "next": None,
            "previous": None,
            "results": [
                {
                    "uuid": "specific-uuid",
                    "name": "Temba Classifier",
                    "intents": ["book_flight", "book_car"],
                    "type": "wit",
                    "created_on": "2013-02-27T09:06:15.456"
                }
            ]
        }
        m.get('https://textit.in/api/v2/classifiers.json?uuid=specific-uuid', json=api_response)

        # Call the list_all_classifiers function with a UUID filter
        result = self.textit.list_all_classifiers(uuid="specific-uuid")

        # Convert result to list of dicts for comparison
        result_data_dicts = result.to_dicts()
        expected_data_dicts = api_response['results']

        # Assert the result matches the expected output
        self.assertEqual(expected_data_dicts, result_data_dicts)