# CDO Framework

This framework exists as a way to interact with the Cisco Defense Orhcestrator API.

## Current Server Information

Multiple API endpoints exist for Cisco, listed is the North America endpoint:
- North America - https://edge.us.cdo.cisco.com/api/public

## Configuration of credential storage

API Credentials are structured in the same format as `configuration_template.json` and are to be placed in a file named `configuration.json`.

## Configuration of main object

Instantiate the CDO object by passing the username configuration from `configuration.json` under the `users` parameter.

Test user-token is named "your_username" in the `configuration_template.json` file.
```python
# Instantiate CDO object
c = CDO(config='your_username')

```

After the object has authenticated to the CDO API, queries may be executed to an API service.

A query made to the CDO API for a list of devices that have been configured :
```python
# Store list of devices
d = c.get_device_list()
print(f'[I] Found {len(d)} results!')
```

Further functions are under development.
- Querying Tenant and Tenant Settings
- Querying Objects
