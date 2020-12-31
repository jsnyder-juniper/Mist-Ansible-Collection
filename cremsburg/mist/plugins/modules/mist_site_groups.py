#!/usr/bin/python

# Copyright: (c) 2020, Calvin Remsburg (@cremsburg) <cremsburg@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: mist_wlan

short_description: Manage lifecycle of Site Groups within your Mist organization.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.4"

description: This module will leverage Mist's REST API to automate the lifecycle management of your Site Groups in Mist.

options:
    api_token:
        description:
            - API token, used for authentication
            - can be stored as an environmental (MIST_API_KEY or MIST_API_TOKEN)
            - please consider using Ansible Vault or some other secure vault for this variable
        required: true
        type: str
    name:
        required: false
        type: str
    org_id:
        description:
            - your Mist Organization ID
            - can be found @ https://api.mist.com/api/v1/self
            - can leverage an environment of MIST_ORG_ID on your Ansible host
        required: true
        type: str
    site_ids:
        description:
            - to be determined, i don't have a working use case where this list was filled
        required: false
        type: list
        elements: str
    state:
        description:
            - create or destroy this site_group
        required: true
        choices: ['absent', 'present']
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - cremsburg.mist.mist_site_groups

author:
    - Calvin Remsburg (@cremsburg)
'''

EXAMPLES = r'''
### #################################################################
### # Create a site
### # assumes org_id and api_token are stored as environmentals
### # on the Ansible host, MIST_ORG_ID and MIST_API_KEY respectively
### #################################################################
- name: Create a new Site Group
  cremsburg.mist.mist_site_groups:
    name: "Burnt Tomato"
    state: "present"

### #################################################################
### # Delete a site
### # here we will pass our org_id and api_token as variable
### # assumes you're storing these variables in some secrets Vault
### #################################################################
- name: Delete an existing Site Group
  cremsburg.mist.mist_site_groups:
    name: "Burnt Tomato"
    state: "absent"

### #################################################################
### # Create the whole enchilla of the site groups
### # passes org_id and api_token in plain text
### # please don't do this, protect your secrets
### #################################################################
- name: Create a new Site Group
  cremsburg.mist.mist_site_groups:
    name: "Burnt Tomato"
    state: "present"
    org_id: "my-organization-id"
    api_token: "my-super-secret-api-key"
'''


from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cremsburg.mist.plugins.module_utils.network.mist.api import MistHelper
from ansible.module_utils._text import to_native


def core(module):
    org_id = module.params['org_id']

    rest = MistHelper(module)

    # ### ##############################################################################################
    # ### # we need to find out of the Site Group already exists within the organization. to accomplish
    # ### #   this task, we will be making an API call to the sitegroups URI endpoint. we create a new
    # ### #   object named site_groups and store the result of our API call
    # ### # we assert that the response code from Mist's API is 200, anything else will fail the module
    # ### ##############################################################################################
    response = rest.get(f"orgs/{org_id}/sitegroups")
    if response.status_code != 200:
        module.fail_json(msg=f"Failed to receive information about the current site groups, here is the response information: {response.info}")

    site_groups = response.json

    # ### ##############################################################################################
    # ### # simply looking to validate that the object returned is in a list format since we will be
    # ### # looping over the object in the very next step
    # ### ##############################################################################################
    if isinstance(site_groups, list):
        pass
    else:
        module.fail_json(msg=f"The site_groups returned from the API are not in a list format, contant Mist support: {site_groups}")

    # ### ##############################################################################################
    # ### # this block of code will validate whether or not the Site Group already exists.
    # ### # create a new empty dictionary called site_group, and give it two keys of 'provisioned' and
    # ### #   'id', and default values of 'False' and 'None', respectively.
    # ### # loop over the returned object from above, and change the values of both keys when a site's
    # ### #   name was a match with what the user had hoped to create. we'll then use this object to
    # ### #   determine how the playbook's next steps are executed (if at all)
    # ### ##############################################################################################
    site_group = dict()
    site_group['provisioned'] = False
    site_group['id'] = None
    for each in site_groups:
        if each['name'] == module.params['name']:
            site_group['provisioned'] = True
            site_group['id'] = each['id']

    # ### ##############################################################################################
    # ### # this is where all the heavy lifting takes place. basing the course of action based upon
    # ### #   the value entered under the parameter's 'state' field, we'll break this up into a simple
    # ### #   'if / else' loop.
    # ### ##############################################################################################
    if module.params['state'] == 'present':

        # ### ######################################################################################
        # ### # we need to check what was entered by the user, determine what needs to be included
        # ### #   within our API call's body. We will be accomplishing this by checking to see
        # ### #   if anything had been entered by the user, and if the value of an object isn't None
        # ### #   then we append the key/value pairs of the data into the previously created empty
        # ### #   dictionary naemd module_parameters.
        # ### # we also need to intentionally prevent the k/v pairs of api_token and org_id from
        # ### #   the payload, because Mist will actually store this a valid data; security risk!
        # ### # it is this object (with data entered from the user) that will be passed to the API
        # ### ######################################################################################
        module_parameters = dict()

        parameters = module.params.items()
        for key, value in parameters:
            if value is not None:
                if key != 'api_token' and key != 'org_id' and key != 'state':
                    module_parameters[key] = value

        # ### ######################################################################################
        # ### # Simple loop to determine if we need to create a new Site Group (POST) or edit an
        # ### #   existing Site Group (PUT).
        # ### # As of this release, a PUT operation will always return a "Changed". some thoughts
        # ### #   will be given at a later date to make this more accurate.
        # ### ######################################################################################
        if site_group['provisioned'] is True:
            # ### ######################################################################################
            # ### # commenting out the api call until i see a need otherwise
            # ### ######################################################################################
            # response = rest.put(f"/orgs/{org_id}/sitegroups/{site_group['id']}", data=module_parameters)
            module.exit_json(changed=False, data=response.json)
        else:
            response = rest.post(f"/orgs/{org_id}/sitegroups", data=module_parameters)
            module.exit_json(changed=True, data=response.json)

    else:

        # ### ######################################################################################
        # ### # Simple loop to determine if we need to delete an existing Site Group (DELETE)
        # ### #   or exiting without taking any action (skipped)
        # ### ######################################################################################
        if site_group['provisioned'] is True:
            response = rest.delete(f"/orgs/{org_id}/sitegroups/{site_group['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data={})


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
    argument_spec = MistHelper.mist_site_groups_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == '__main__':
    main()
