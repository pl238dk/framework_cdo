import json
import requests
requests.packages.urllib3.disable_warnings()

class CDO(object):
	def __init__(self, config=None):
		self.base_url = 'https://edge.us.cdo.cisco.com/api/public'
		if config is None:
			print('[E] No configuration filename not provided')
		else:
			self.load_configuration(config)
		return
	
	def load_configuration(self, config):
		import os
		config_file = 'configuration.json'
		path = os.path.abspath(__file__)
		dir_path = os.path.dirname(path)
		with open(f'{dir_path}/{config_file}','r') as f:
			raw_file = f.read()
		config_raw = json.loads(raw_file)
		if config not in config_raw['users']:
			print('[E] Configuration not found in configuration.json')
		else:
			token = config_raw['users'][config]['token']
			self.session = requests.Session()
			self.session.trust_env = False
			proxies = {
				'http':'',
				'https':'',
			}
			self.session.proxies = proxies
			headers = {
				'Authorization': f'Bearer {token}'
			}
			self.session.headers = headers
		return
	
	def post(self, query):
		query = {'query': query}
		response_raw = self.session.post(
			self.base_url,
			json=query,
			verify=False
		)
		output = {
			'success': False,
			'result': '',
			'response': response_raw,
		}
		print(f'[D] HTTP POST - {response_raw.status_code}')
		if response_raw.status_code == 200:
			response_json = json.loads(response_raw.text)
			output['result'] = response_json
		return output
	
	def get_device_list(self):
		output = []
		limit = 100
		offset = 0
		count = 0
		query = f'''
			query {{
				devices(limit: {limit}, sortField: NAME, offset: {offset}){{
					metadata {{
						count
					}}
					items {{
						name
					}}
				}}
			}}
		'''
		response = self.post(query)
		count = int(response['result']['data']['devices']['metadata']['count'])
		output.extend(
			response['result']['data']['devices']['items']
		)
		while len(output) < count:
			offset += 100
			query = f'''
				query {{
					devices(limit: {limit}, sortField: NAME, offset: {offset}){{
						metadata {{
							count
						}}
						items {{
							name
						}}
					}}
				}}
			'''
			response = self.post(query)
			output.extend(
				response['result']['data']['devices']['items']
			)
		return output

''' # tenantSettings
query = """
query {
	tenantSettings {
		uid
		enableChangeRequestTracking
		lastUpdatedDate
		preventCiscoSupportFromViewingTenant
		autoDetectRuleSets
		autoAcceptDeviceChanges
		allowDeploymentScheduling
	}
}
"""
#'''

''' # devices
query = """
query {
  devices(limit: 50, sortField: NAME, deviceType: [FIREPOWER, ASA, FTD]) {
    metadata {
      count
    }
    items {
      softwareVersion
      name
      uid
      isModel
      conflictDetectionState
      ipv4
      deviceType
      serial
      configurationStatus
      interfaces
      connectivityState
      highAvailability
      specificDevice {
        namespace
        ... on FtdSpecificDevice {
          uid
        }
        ... on AsaSpecificDevice {
          uid
          type
          vpnId
        }
        ... on MerakiSpecificDevice {
          uid
          type
        }
        ... on AwsSpecificDevice {
          vpcId
          region
        }
      }
    }
  }
}

"""
#'''

''' # objects
query = """
query {
  objects(
    limit: 100
    objectType: [NETWORK_GROUP, NETWORK_OBJECT]
    offset: 42
    sortOrder: DESC
    sortField: OBJECT_TYPE
  ) {
    metadata {
      count
    }
    items {
      name
      uid
      objectType
      description
      details {
        ... on NetworkDetailsBase {
          wildcardMask
        }
        ... on NetworkDetailsIpEq {
          value
        }
        ... on NetworkDetailsIpRange {
          start
          end
        }

        ... on NetworkGroupDetails {
          items {
            ... on ObjectReferenceDetails {
              uid
              name
              type
            }
            ... on NetworkDetailsIpEq {
              value
            }
          }
        }
      }
    }
  }
}
"""
#'''

if __name__ == '__main__':
	c = CDO(config='networkcentral')
	d = c.get_device_list()
	print(f'[I] Found {len(d)} results!')
