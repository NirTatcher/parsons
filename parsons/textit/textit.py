

from parsons.utilities import check_env
from parsons.utilities.api_connector import APIConnector
from parsons import Table

class TextIt:
    def __init__(self, api_key=None):
        self.api_key = check_env.check('TEXTIT_API_KEY', api_key)
        self.uri = 'https://textit.in/api/v2/'
        self.headers = {'Authorization': f'Token {self.api_key}'}
        self.api = APIConnector(self.uri, headers=self.headers)
    def get_archives(self, archive_type=None, before=None, period=None):
        """
        Fetches archives from TextIt.

        `Args:`
            archive_type: str
                The type of archive to fetch. Options include 'message', 'flow', 'run', etc.
            before: str
                The datetime string to fetch archives before this date.
            period: str
                The period to fetch archives for. Options include 'day', 'week', 'month', etc.
        `Returns:`
            Parsons Table
                A Parsons table of the archives.
        """
        params = {}
        if archive_type:
            params['archive_type'] = archive_type
        if before:
            params['before'] = before
        if period:
            params['period'] = period
        all_results = []
        next_url = 'archives.json'
        while next_url:
            response = self.api.get_request(next_url, params=params)
            data = response
            all_results.extend(data['results'])
            next_url = data['next']
        return Table(all_results)
    def get_boundaries(self, geometry=False):
        """
        Fetches administrative boundaries from the TextIt API.

        `Args:`
            geometry: A boolean to specify whether to include simplified GPS geometry
                        for the boundaries in GEOJSON format. Default is False.

        `Returns:`
            A Parsons Table of the boundaries list. Columns include 'osm_id', 'name',

                'parent', 'level', 'geometry' (if requested).
        """
        params = {'geometry': 'true'} if geometry else {}
        all_results = []
        next_url = 'boundaries.json'
        while next_url:
            response = self.api.get_request(next_url, params=params)
            data = response
            all_results.extend(data['results'])
            next_url = data['next']
        return Table(all_results)
   
    def list_broadcasts(self, id=None, before=None, after=None):
        """
        Lists broadcasts with optional filtering.

        `Args:`
            id (int, optional): The ID of the broadcast to filter by.
            before (str, optional): Filter broadcasts created before this datetime.
            after (str, optional): Filter broadcasts created after this datetime.

        `Returns:`
            dict: A dictionary containing the list of broadcasts.
        """
        params = {}
        if id:
            params['id'] = id
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        all_results = []
        next_url = 'broadcasts.json'
        while next_url:
            response = self.api.get_request(next_url, params=params)
            data = response
            all_results.extend(data['results'])
            next_url = data['next']
        return Table(all_results)
    def send_broadcast(self, urns=None, contacts=None, groups=None, text=None, attachments=None, base_language=None):
        """

        Sends a new broadcast.

        `Args:`
            urns (list of str, optional): URNs of contacts to send to.
            contacts (list of str, optional): UUIDs of contacts to send to.
            groups (list of str, optional): UUIDs of contact groups to send to.
            text (dict of str, optional): Message text translations.
            attachments (dict of list of str, optional): Attachment translations.
            base_language (str, optional): The default translation language.

        `Returns:`
            dict: A dictionary containing the broadcast that was created.
        """
        payload = {
            "urns": urns if urns else [],
            "contacts": contacts if contacts else [],
            "groups": groups if groups else [],
            "text": text if text else {},
            "attachments": attachments if attachments else {},
            "base_language": base_language
        }

        response = self.api.post_request('/api/v2/broadcasts.json', json=payload)
        return response
    
    def list_all_campaigns(self, uuid=None, before=None, after=None):
        """
        Fetches all campaigns from TextIt, handling pagination and allowing for filtering.

        Args:
            uuid (str, optional): Filter by the UUID of the campaign.
            before (str, optional): Filter campaigns created before this datetime.
            after (str, optional): Filter campaigns created after this datetime.

        Returns:
            Parsons Table: A Parsons table of all the campaigns.
        """
        params = {}
        if uuid:
            params['uuid'] = uuid
        if before:
            params['before'] = before
        if after:
            params['after'] = after

        all_results = []
        next_url = 'campaigns.json'

        while next_url:
            response = self.api.get_request(next_url, params=params)
            data = response
            all_results.extend(data['results'])
            next_url = data['next']  # This is typically a full URL provided by the API

        return Table(all_results)
    
    def add_campaign(self, name, group_uuid):
        """
        Adds a new campaign to TextIt.

        Args:
            name (str): The name of the campaign.
            group_uuid (str): The UUID of the contact group this campaign will be run against.

        Returns:
            dict: A dictionary containing the details of the campaign that was created.
        """
        payload = {
            "name": name,
            "group": group_uuid
        }

        response = self.api.post_request('campaigns.json', json=payload)
        return response
    
    def update_campaign(self, uuid, name=None, group_uuid=None):
        """
        Updates an existing campaign in TextIt.

        Args:
            uuid (str): The UUID of the campaign to update.
            name (str, optional): The new name of the campaign.
            group_uuid (str, optional): The new UUID of the contact group this campaign will target.

        Returns:
            The response from the API without converting it to JSON, as this is handled by the post_request function.
        """
        payload = {}
        if name:
            payload['name'] = name
        if group_uuid:
            payload['group'] = group_uuid

        return self.api.post_request(f'campaigns.json?uuid={uuid}', json=payload)
    
    def list_all_campaign_events(self, uuid=None, campaign_uuid=None):
        """
        Fetches all campaign events from TextIt, handling pagination and allowing for filtering by either the campaign event's UUID or the campaign's UUID.

        Args:
            uuid (str, optional): The UUID of the specific campaign event to filter by.
            campaign_uuid (str, optional): The UUID of the campaign to filter campaign events by.

        Returns:
            Parsons Table: A Parsons table of all the campaign events, including details such as the campaign event UUID, campaign details, relative_to, offset, unit, delivery_hour, message, flow, and created_on.
        """
        params = {}
        if uuid:
            params['uuid'] = uuid
        if campaign_uuid:
            params['campaign'] = campaign_uuid

        all_results = []
        next_url = 'campaign_events.json'

        while next_url:
            response = self.api.get_request(next_url, params=params)
            data = response
            all_results.extend(data['results'])
            next_url = data['next']

        return Table(all_results)
    
    def add_campaign_event(self, campaign, relative_to, offset, unit, delivery_hour=-1, message=None, flow=None):
        """
        Adds a new campaign event.

        Args:
            campaign (str): The UUID of the campaign this event should be part of.
            relative_to (str): The field key that this event will be relative to.
            offset (int): The offset from our contact field (positive or negative integer).
            unit (str): The unit for our offset (one of "minutes", "hours", "days", "weeks").
            delivery_hour (int, optional): The hour of the day to deliver the message. Defaults to -1.
            message (str, optional): The message to send to the contact.
            flow (str, optional): The UUID of the flow to start the contact down.

        Returns:
            dict: A dictionary containing the details of the campaign event that was created.
        """
        payload = {
            "campaign": campaign,
            "relative_to": relative_to,
            "offset": offset,
            "unit": unit,
            "delivery_hour": delivery_hour,
            "message": message,
            "flow": flow
        }

        response = self.api.post_request('campaign_events.json', json=payload)
        return response
    
    def update_campaign_event(self, uuid, relative_to=None, offset=None, unit=None, delivery_hour=None, message=None, flow=None):
        """
        Updates an existing campaign event.

        Args:
            uuid (str): The UUID of the campaign event to update.
            relative_to (str, optional): The new field key that this event will be relative to.
            offset (int, optional): The new offset from our contact field.
            unit (str, optional): The new unit for our offset.
            delivery_hour (int, optional): The new hour of the day to deliver the message.
            message (str, optional): The new message to send to the contact.
            flow (str, optional): The new UUID of the flow to start the contact down.

        Returns:
            The response from the API without converting it to JSON, as this is handled by the post_request function.
        """
        payload = {
            "relative_to": relative_to,
            "offset": offset,
            "unit": unit,
            "delivery_hour": delivery_hour,
            "message": message,
            "flow": flow
        }

        return self.api.post_request(f'campaign_events.json?uuid={uuid}', json=payload)
    
    def delete_campaign_event(self, uuid):
        """
        Deletes a campaign event.

        Args:
            uuid (str): The UUID of the campaign event to delete.

        Returns:
            The response from the API without converting it to JSON, as this is handled by the delete_request function.
        """
        return self.api.delete_request(f'campaign_events.json?uuid={uuid}')
    
    def list_all_channels(self, uuid=None, address=None):
        """
        Fetches all channels from TextIt, handling pagination and allowing for filtering.

        Args:
            uuid (str, optional): Filter by the UUID of the channel.
            address (str, optional): Filter by the address of the channel.

        Returns:
            Parsons Table: A Parsons table of all the channels.
        """
        params = {}
        if uuid:
            params['uuid'] = uuid
        if address:
            params['address'] = address

        all_results = []
        next_url = '/api/v2/channels.json'

        while next_url:
            response = self.api.get_request(next_url, params=params)
            data = response
            all_results.extend(data['results'])
            next_url = data['next']

        return Table(all_results)
    
    def list_all_channel_events(self, id=None, contact=None, before=None, after=None):
        """
        Fetches all channel events from TextIt, handling pagination and allowing for filtering.

        Args:
            id (int, optional): Filter by the ID of the event.
            contact (str, optional): Filter by the UUID of the contact.
            before (str, optional): Filter events created before a certain datetime.
            after (str, optional): Filter events created after a certain datetime.

        Returns:
            Parsons Table: A Parsons table of all the channel events.
        """
        params = {}
        if id:
            params['id'] = id
        if contact:
            params['contact'] = contact
        if before:
            params['before'] = before
        if after:
            params['after'] = after

        all_results = []
        next_url = 'channel_events.json'

        while next_url:
            response = self.api.get_request(next_url, params=params)
            data = response
            all_results.extend(data['results'])
            next_url = data['next']

        return all_results


    def list_all_classifiers(self):
        """
        Fetches all classifiers from TextIt, handling pagination.

        Returns:
            list: A list of all the classifiers.
        """
        all_results = []
        next_url = f"{self.base_url}/classifiers.json"

        while next_url:
            response = requests.get(next_url, headers={"Authorization": f"Token {self.api_key}"})
            data = response.json()
            all_results.extend(data['results'])
            next_url = data.get('next')

        return all_results

    def list_all_classifiers(self, uuid=None):
        """
        Fetches all classifiers from TextIt, handling pagination and allowing for filtering by UUID.

        Args:
            uuid (str, optional): Filter by the UUID of the classifier.

        Returns:
            Parsons Table: A Parsons table of all the classifiers.
        """
        params = {}
        if uuid:
            params['uuid'] = uuid

        all_results = []
        next_url = 'classifiers.json'

        while next_url:
            response = self.api.get_request(next_url, params=params)  # Adjusted to include params
            all_results.extend(response['results'])
            next_url = response['next']

        return Table(all_results)



    def list_all_contacts(self, uuid=None, urn=None, group=None, before=None, after=None):
        """
        Fetches all contacts from TextIt, handling pagination and allowing for filtering by various parameters.

        Args:
            uuid (str, optional): Filter by the UUID of the contact.
            urn (str, optional): Filter by the URN of the contact.
            group (str, optional): Filter by the group name or UUID the contact is part of.
            before (str, optional): Filter contacts modified before a certain datetime.
            after (str, optional): Filter contacts modified after a certain datetime.

        Returns:
            Parsons Table: A Parsons table of all the contacts.
        """
        params = {}
        if uuid:
            params['uuid'] = uuid
        if urn:
            params['urn'] = urn
        if group:
            params['group'] = group
        if before:
            params['before'] = before
        if after:
            params['after'] = after

        all_results = []
        next_url = 'contacts.json'

        while next_url:
            response = self.api.get_request(next_url, params=params)
            all_results.extend(response['results'])
            next_url = response['next']

        return Table(all_results)
    
    def add_contact(self, name=None, language=None, urns=None, groups=None, fields=None):
        """
        Adds a new contact to TextIt.

        Args:
            name (str, optional): The full name of the contact.
            language (str, optional): The preferred language for the contact (3 letter ISO code).
            urns (list of str, optional): A list of URNs to associate with the contact.
            groups (list of str, optional): A list of the UUIDs of any groups this contact is part of.
            fields (dict, optional): The contact fields to set or update on this contact.

        Returns:
            dict: A dictionary containing the details of the contact that was created.
        """
        payload = {
            "name": name,
            "language": language,
            "urns": urns if urns else [],
            "groups": groups if groups else [],
            "fields": fields if fields else {}
        }

        response = self.api.post_request('contacts.json', json=payload)
        return response
    
    def update_contact(self, identifier, identifier_type='uuid', name=None, language=None, urns=None, groups=None, fields=None):
        """
        Updates an existing contact in TextIt.

        Args:
            identifier (str): The UUID or URN of the contact to update.
            identifier_type (str, optional): Specifies if the identifier is a 'uuid' or 'urn'. Defaults to 'uuid'.
            name (str, optional): The full name of the contact.
            language (str, optional): The preferred language for the contact (3 letter ISO code).
            urns (list of str, optional): A list of URNs to associate with the contact. Should not be used if identifier_type is 'urn'.
            groups (list of str or dict, optional): A list of the UUIDs or dict of groups this contact is part of.
            fields (dict, optional): The contact fields to set or update on this contact.

        Returns:
            dict: A dictionary containing the details of the updated contact.
        """
        if identifier_type not in ['uuid', 'urn']:
            raise ValueError("identifier_type must be either 'uuid' or 'urn'")

        payload = {}
        if name:
            payload['name'] = name
        if language:
            payload['language'] = language
        if urns and identifier_type != 'urn':
            payload['urns'] = urns
        if groups:
            payload['groups'] = groups
        if fields:
            payload['fields'] = fields

        if identifier_type == 'uuid':
            response = self.api.post_request(f'contacts.json?uuid={identifier}', json=payload)
        else:  # 'urn'
            response = self.api.post_request(f'contacts.json?urn={identifier}', json=payload)

        return response
    
    