#!/usr/bin/python

# Copyright: (c) 2020, Calvin Remsburg (@cremsburg) <cremsburg@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: mist_site

short_description: Manage lifecycle of sites within your Mist organization.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description: This module will leverage Mist's REST API to automate the lifecycle management of your sites in Mist.

options:
    address:
        description: full address of the site
        required: false
        type: str
    alarmtemplate_id:
        description: Alarm Template ID, this takes precedence over the Org-level alarmtemplate_id
        required: false
        type: str
    api_token:
        description:
            - API token, used for authentication
            - can be stored as an environmental (MIST_API_KEY or MIST_API_TOKEN)
            - please consider using Ansible Vault or some other secure vault for this variable
        required: true
        type: str
    country_code:
        description:
            - country code for the site (for AP config generation)
            - use two-character notation: US
        required: false
        type: str
    latlng:
        description:
            - pass the site's coordinates in the format of a dictionary
            - requires a float value for "lat" and "lng" keys
        required: false
        type: dict
        suboptions:
            lat:
                description:
                    - latitude in float notation
                required: true
                type: float
            lng:
                description:
                    - longitude in float notation
                required: true
                type: float
    name:
        description:
            - the name of your site
            - will be used as a parameter when determining if the site already exists
            - does not support duplicate site names in same organization
        required: true
        type: str
    notes:
        description:
            - optional, any notes about the site
        required: false
        type: str
    org_id:
        description:
            - your Mist Organization ID
            - can be found @ https://api.mist.com/api/v1/self
            - can leverage an environment of MIST_ORG_ID on your Ansible host
        required: true
        type: str
    rftemplate_id:
        description:
            - RF Template ID
            - takes precedence over Site Settings
        required: false
        type: str
    secpolicy_id:
        description:
            - SecPolicy ID
        required: false
        type: str
    sitegroup_ids:
        description:
            - sitegroups this site belongs to
        required: false
        type: list
        elements: str
    state:
        description:
            - control whether the site name should exist in Mist
            - choices are "present" for affirmative and "absent" for negative
        required: false
        type: str
    timeout:
        description:
            - how long the API should wait for a response before giving up
        required: false
        type: int
    timezone:
        description:
            - the timezone for the site's location
        required: false
        type: str
    validate_certs:
        description:
            - whether or not the certificate at https://api.mist/com is valid
            - may help those behind proxies
        required: false
        default: true
        type: bool

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - cremsburg.mist.mist_site

author:
    - Calvin Remsburg (@cremsburg)
'''

EXAMPLES = r'''
### #################################################################
### # Create a site
### # assumes org_id and api_token are stored as environmentals
### # on the Ansible host, MIST_ORG_ID and MIST_API_KEY respectively
### #################################################################
- name: Create a new site
  cremsburg.mist.mist_site:
    name: "katy"
    address: "410 Mason Rd, Katy, TX 77450, USA"
    latlng:
        lat: 29.778506,
        lng: -95.752323
    state: "present"

### #################################################################
### # Delete a site
### # here we will pass our org_id and api_token as variable
### # assumes you're storing these variables in some secrets Vault
### #################################################################
- name: Delete an existing site
  cremsburg.mist.mist_site:
    name: "katy"
    state: "absent"
    org_id: "{{ org_id }}"
    api_token: "{{ api_token }}"

### #################################################################
### # Create the whole enchilla of the site
### # passes org_id and api_token in plain text
### # please don't do this, protect your secrets
### #################################################################
- name: Create a new site
  cremsburg.mist.mist_site:
    name: "katy"
    address: "410 Mason Rd, Katy, TX 77450, USA"
    alarmtemplate_id: "1234567890"
    country_code: "US"
    latlng:
        lat: 29.778506,
        lng: -95.752323
    notes: "i'm just a note, yes i'm only a note, and i'm sitting here on ansible docs"
    org_id: "12345678-910a-bcde-fghi-jklmnopqrstu"
    rftemplate_id: "1234567890"
    secpolicy_id: "1234567890"
    sitegroup_ids:
        - "1234567890"
    state: "present"
    timeout: 30
    timezone: "America/Chicago"
    validate_certs: False
    api_token: "loremipsumdolorsitametloremipsumdolorsitametloremipsumdolorsitametloremipsumdol"
'''


from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cremsburg.mist.plugins.module_utils.network.mist.api import MistHelper
from ansible.module_utils._text import to_native


def core(module):
    # ### ########################################################################
    # ### # setting the stage. we create the following:
    # ### #   - name: the site's name, entered by the user
    # ### #   - org_id: set by the environmental or within teh module
    # ### #   - rest: this is where we take in AnsibleModule class created earlier
    # ### #           in the main function, when we inserted our argument spec
    # ### #           into it. we'll use new object for all API calls
    # ### ########################################################################
    name = module.params['name']
    org_id = module.params['org_id']
    rest = MistHelper(module)

    # ### ########################################################################
    # ### # gather a list of sites already created
    # ### # make sure the status code received was a 200
    # ### # store the list of sites in a new object called 'sites', make sure that
    # ### #   the object is in the format of a list, since we'll be looping soon
    # ### ########################################################################
    response = rest.get(f"orgs/{org_id}/sites")
    if response.status_code != 200:
        module.fail_json(msg=f"Failed to receive information about the current sites, here is the response information to help you debug : {response.info}")

    sites = response.json

    if isinstance(sites, list):
        pass
    else:
        module.fail_json(msg=f"The sites returned from the API are not in a list format, contant Mist support: {sites}")

    # ### ########################################################################
    # ### # it's important to know if the site has already been provisioned, as
    # ### #   this will shape our future API calls. we create a new dictionary
    # ### #   with a k/v of 'provisioned' set to False. if the site has already
    # ### #   been provisioned, we'll flip this bit to True and store it's site ID
    # ### ########################################################################
    site = dict()
    site['provisioned'] = False
    site['id'] = None
    for each in sites:
        if each['name'] == name:
            site['provisioned'] = True
            site['id'] = each['id']

    # ### ########################################################################
    # ### # if the user set the state to 'absent', then we need to either delete
    # ### #   an existing site, or report back to the user that the site didn't
    # ### #   exist.
    # ### ########################################################################
    if module.params['state'] == "absent":
        if site['provisioned'] is True:
            response = rest.delete(f"/sites/{site['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data="site does not exist, exiting")

    # ### ########################################################################
    # ### # if the user set the state to 'present', then we need to either create
    # ### #   a new site or edit an existing one.
    # ### # this logic can get a little harry, so stick with the comments when
    # ### #   you're deep in the woods and need a guiding light
    # ### ########################################################################
    else:

        # ### ########################################################################
        # ### # create the site if it doesn't already exist
        # ### ########################################################################
        if site['provisioned'] is False:

            # ### ########################################################################
            # ### # we create a few important objects here:
            # ### #   - site_data: parameters entered by the user to create the site
            # ### #   - response: create the site and store the response of our API
            # ### #   - site['id']: use the response to get the site's id
            # ### #                 parent object site was created above
            # ### ########################################################################
            site_data = dict(name=name,
                             address=module.params['address'],
                             alarmtemplate_id=module.params['alarmtemplate_id'],
                             country_code=module.params['country_code'],
                             latlng=module.params['latlng'],
                             notes=module.params['notes'],
                             rftemplate_id=module.params['rftemplate_id'],
                             secpolicy_id=module.params['secpolicy_id'],
                             timezone=module.params['timezone'])
            response = rest.post(f"orgs/{org_id}/sites", data=site_data)
            site['id'] = response.json['id']

        # ### ########################################################################
        # ### # create a few important objects before we get into the logic
        # ### #   - site_groups: this will flip it to true if there was data entered
        # ### #                  by the user in the 'sitegroups' parameter
        # ### #   - payload: this will be the json payload that's pushed to Mist
        # ### #              we will fill this dictionary in the for loop below
        # ### #   - parameters: the data entered by the user in the Ansible Module
        # ### ########################################################################
        site_groups = False
        payload = dict()
        parameters = module.params.items()

        # ### ########################################################################
        # ### # look at all of the data entered by the user by iterating over the
        # ### #   parameters object created above. we will only want an object that
        # ### #   has data entered within them, we do this by making sure the value
        # ### #   of each parameter is not None (null).
        # ### # we also exclude things like the API token, Org ID, and sitegroups.
        # ### #   the reason we make this exception for sitegroups is becase we can't
        # ### #   simply pass in the friendly names into the payload, we need to
        # ### #   translate them into the ID string that Mist will understand.
        # ### ########################################################################
        for key, value in parameters:
            if value is not None:
                if key != 'api_token' and key != 'org_id' and key != 'sitegroups':
                    payload[key] = value
                # this is where we flag if there was data in the sitegroups parameter
                elif key == 'sitegroups':
                    site_groups = True

        # ### ########################################################################
        # ### # if, at any time, the value of site_groups was flipped to true in the
        # ### #   previous loop, we know that the user is looking to add this site
        # ### #   to an existing site_group.
        # ### # this section's goal is to translation a Site Group's names to an ID
        # ### #   to accomplish our goals
        # ### ########################################################################
        if site_groups is True:

            # ### ########################################################################
            # ### # create a few more critical objects
            # ### #   - id_list: a list of IDs, translated from the site's name
            # ### #   - params: the list of friendly Site Group names entered by the user
            # ### #   - provisioned: a collection of current Site Group objects
            # ### ########################################################################
            id_list = list()
            params = module.params['sitegroups']
            provisioned = rest.get(f"/orgs/{org_id}/sitegroups")

            # ### ########################################################################
            # ### # try to match a Site Group name entered by the user to an existing
            # ### #   Site Group ID
            # ### # all matches will be appended to our, previously empty, id_list
            # ### ########################################################################
            for each in params:
                for current in provisioned.json:
                    if each == current['name']:
                        id_list.append(current['id'])

            # ### ########################################################################
            # ### # we finally have everything we need. let's create a final object named
            # ### #   payload. it'll be a dictionary with the key of 'sitegroup_ids' and
            # ### #   the value will be our list.
            # ### # this will be converted into the exact JSON payload that Mist expects
            # ### ########################################################################
            payload = dict()
            payload['sitegroup_ids'] = id_list

            # ### ########################################################################
            # ### # last step, oofta. grab the response object from earlier and set the
            # ### #   value of site_id to that of it's id key. then we pass it the
            # ### #   list of site groups in the correct format, created in teh step above
            # ### ########################################################################
            response = rest.put(f"sites/{site['id']}", data=payload)
            module.exit_json(changed=True, data=response.json)

        else:
            module.exit_json(changed=True, data=response.json)


def main():
    # ### ########################################################################
    # ### # this is the main function, did the name give it away?
    # ### # we're taking in the Module's argument spec from the MistHelper and
    # ### #   saving it as a new object named 'argument_spec'.
    # ### # another object is created, this time to the specification defined by
    # ### #   the offical AnsibleModule class, and we pass in the argument_spec.
    # ### #   this act creates our new 'module' object, which is then passed
    # ### #   through our other, much larger, function named 'core'
    # ### ########################################################################
    argument_spec = MistHelper.mist_site_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == '__main__':
    main()
