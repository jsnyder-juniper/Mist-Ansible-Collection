#!/usr/bin/python

# Copyright: (c) 2020, Calvin Remsburg (@cremsburg) <cremsburg@protonmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: mist_wired

short_description: Manage configuration of switches within your Mist organization.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description: This module will leverage Mist's REST API to automate the lifecycle management of your switch configurations in Mist.

options:
    additional_config_cmds:
        description:
            - Junos configurations in "set" format
        required: false
        type: list

    api_token:
        description:
            - API token, used for authentication
            - can be stored as an environmental (MIST_API_KEY or MIST_API_TOKEN)
            - please consider using Ansible Vault or some other secure vault for this variable
        required: true
        type: str

    disable_auto_config:
        required: false
        type: bool

    ip_config:
        description:
            - layer 3 interface configuration
            - this is the inband management
        required: false
        elements: dict
        suboptions:
            network:
                required: false
                type: str
            type:
                required: false
                type: str

    networks:
        description:
            - state your VLANs here
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                required: false
                type: str
            vlan_id:
                required: false
                type: str

    notes:
        description:
            - some helpful notes
            - can be used to provide more documentation
        required: false
        type: str

    oob_ip_config:
        description:
            - layer 3 interface configuration
            - this is the out-of-band management
        required: false
        elements: dict
        suboptions:
            network:
                required: false
                type: str
            type:
                required: false
                type: str

    port_config:
        description:
            - interface configuration goes here
            - name will be either the interface or range of interfaces
            - profile is the port-profile applied to this interface
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                required: false
                type: str
            profile:
                required: false
                type: str

    port_profiles:
        description:
            - Port Profiles, your interface configuration templates
        required: false
        type: list
        elements: dict
        suboptions:
            all_networks:
                required: false
                type: bool
            disabled:
                required: false
                type: bool
            duplex:
                required: false
                type: str
            mac_limit:
                required: false
                type: int
            mode:
                required: false
                type: str
                choices: ['access', 'trunk']
            name:
                required: false
                type: str
            networks:
                required: false
                type: list
            poe_disabled:
                required: false
                type: bool
            port_auth:
                required: false
                type: dict
            port_network:
                required: false
                type: str
            speed:
                required: false
                type: str
            stp_edge:
                required: false
                type: bool
            voip_network:
                required: false
                type: str

    org_id:
        description:
            - your Mist Organization ID
            - can be found @ https://api.mist.com/api/v1/self
            - can leverage an environment of MIST_ORG_ID on your Ansible host
        required: true
        type: str

    role:
        description:
            - role for the switch
        required: false
        type: str

    site_id:
        description:
            - id of the site
            - note: this is faster than using the site_name option
        required: false
        type: str

    site_name:
        description:
            - name of the site
            - note: this is slower than using the site_id option
            -   it requires an additional API lookup to find the site_id
        required: false
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - cremsburg.mist.mist_wired

author:
    - Calvin Remsburg (@cremsburg)
'''

EXAMPLES = r'''
### #################################################################
### # Configure a switch
### #################################################################
    - name: configure a switch
      cremsburg.mist.mist_wired:
        name: Katy-SW1
        id: 00000000-0000-0000-1000-123456789010
        site_id: 71168e39-1234-1234-1234-123456789010
        ip_config:
            type: dhcp
            network: default
        networks:
          - name: home
            vlan_id: "91"
        port_config:
          - name: ge-0/0/0
            profile: mist-ap
          - name: ge-0/0/1
            profile: home
        port_profiles:
          - name: home
            mode: access
            disabled: False
            port_network: "home"
            stp_edge: True
            poe_disabled: True

### #################################################################
### # Create the whole enchilla
### #################################################################
    - name: configure a switch
      cremsburg.mist.mist_wired:
        name: Katy-SW1
        id: 00000000-0000-0000-1000-123456789010
        site_id: 71168e39-1234-1234-1234-123456789010
        ip_config:
          type: dhcp
          network: default
        oob_ip_config:
          type: dhcp
          network: default
        networks:
          - name: home
            vlan_id: "91"
          - name: devops
            vlan_id: "101"
        port_config:
          - name: ge-0/0/0
            profile: mist-ap
          - name: ge-0/0/1
            profile: home
        port_profiles:
          - name: home
            mode: access
            disabled: False
            port_network: "home"
            stp_edge: True
            poe_disabled: True
          - name: mist-ap
            mode: trunk
            all_networks: True
            disabled: False
            port_network: "home"
            stp_edge: True
            poe_disabled: False
        org_id: "12345678-910a-bcde-fghi-jklmnopqrstu"
        api_token: "loremipsumdolorsitametloremipsumdolorsitametloremipsumdolorsitametloremipsumdol"
'''


from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cremsburg.mist.plugins.module_utils.network.mist.api import MistHelper
from ansible.module_utils._text import to_native


def core(module):
    org_id = module.params['org_id']

    rest = MistHelper(module)

    try:
        site_id = module.params['site_id']
    except KeyError:
        site_id = None

    # ### ##########################################################################################
    # ### error the module out if a user didn't add a site_id or site_name
    # ### ##########################################################################################
    if site_id is None:

        # ### ##########################################################################################
        # ### collect a list of the sites already present within the organization
        # ### create a new object called 'sites' that will hold the sites returned from the API
        # ### validate that the objects 'sites' is in list format, since we are about to loop over it
        # ### ##########################################################################################
        response = rest.get(f"orgs/{org_id}/sites")
        if response.status_code != 200:
            module.fail_json(msg=f"Failed to receive information about the current sites, here is the response: {response.info}")

        sites = response.json

        if isinstance(sites, list):
            pass
        else:
            module.fail_json(msg=f"The sites returned from the API are not in a list format, contant Mist support: {sites}")

        # ### ##########################################################################################
        # ### # translate the site name to a site_id
        # ### ##########################################################################################
        try:
            site_name = module.params['site_name']
            site_id = ""
            for each in sites:
                if each['name'] == site_name:
                    site_id = each['id']
        except KeyError:
            module.fail_json(msg=f"You need to pass either a site_id or site-name parameter: {response.info}")

        if site_id == "":
            module.fail_json(msg=f"You selected a site that does not exist. Here's the list we got back from Mist: {sites}")

    # gather a list of devices already created at the org-level
    response = rest.get(f"orgs/{org_id}/inventory?vc=true")
    if response.status_code != 200:
        module.fail_json(msg=f"Failed to receive information about the current inventory, here is the response information to help you debug : {response.info}")

    # save the output of our API call to a new object called sites
    inventory = response.json

    # check to see if the inventory object is a list, fail the module if the return payload is anything else
    if isinstance(inventory, list):
        pass
    else:
        module.fail_json(msg=f"The inventory returned from the API are not in a list format, contant Mist support: {inventory}")

    # ### ########################################################################
    # ### # it's important to know if the device is online and provisioned
    # ### # we accomplish this task by creating a new dictionary
    # ### #   with a k/v of 'provisioned' set to False. if the site has already
    # ### #   been provisioned, we'll flip this bit to True and store it's site ID
    # ### ########################################################################
    switch = dict()
    switch['provisioned'] = False
    switch['id'] = None
    for each in inventory:
        if each['type'] == 'switch':
            try:
                if each['name'] == module.params['name']:
                    switch['provisioned'] = True
                    switch['id'] = each['id']
            except KeyError:
                pass

    # ### #################################################################################
    # ### # create an empty object to store configuration parameters, fed to it in the
    # ### #   Ansible Module's parameters.
    # ### # this is the python dictionary that will be converted to JSON before pushing
    # ### #   to the Mist API.
    # ### # this dictionary will undergo several facelifts to make it align perfectly to
    # ### #   what mist is expecting.
    # ### #################################################################################
    switch_config = dict()

    # ### #################################################################################
    # ### # set the key/value pairs of the parameters to a new object
    # ### # iterate over the object, look to see if anything was entered, if there was
    # ### #   something added by the user, append it to our empty dict
    # ### #################################################################################
    parameters = module.params.items()
    for key, value in parameters:
        if value is not None:
            switch_config[key] = value

    # ### #################################################################################
    # ### # pop off unnessesary baggage
    # ### #################################################################################
    switch_config.pop('api_token')
    switch_config.pop('org_id')
    try:
        switch_config.pop('site_id')
    except KeyError:
        pass

    # ### #################################################################################
    # ### # change up some of the parameters to make it Mist API friendly, specifically the
    # ### #   networks will be translated from a list into a dictionary. this is to address
    # ### #   the fact that the API uses the name of a network as the key, and that's
    # ### #   simply impossible to address as an Ansible argument spect
    # ### #################################################################################
    mist_friendly_networks = dict()
    for each in switch_config['networks']:
        network = dict()
        network[each['name']] = dict()
        network[each['name']]['vlan_id'] = each['vlan_id']
        mist_friendly_networks.update(network)

    switch_config['networks'] = mist_friendly_networks

    # ### #################################################################################
    # ### # same as the situation above. our module takes in a list and here we'll flip it
    # ### #   into a dictionary to allow for key's to bear the name of the interface.
    # ### #################################################################################
    mist_friendly_port_config = dict()
    for each in switch_config['port_config']:
        interface_config = dict()
        interface_config[each['name']] = dict()
        interface_config[each['name']]['usage'] = each['profile']
        mist_friendly_port_config.update(interface_config)

    switch_config['port_config'] = mist_friendly_port_config

    # ### #################################################################################
    # ### # so, here we meet again. same issue, this time for port_profiles
    # ### #################################################################################
    mist_friendly_port_profiles = dict()
    for each in switch_config['port_profiles']:
        port_profile = dict()
        port_profile[each['name']] = dict()
        port_profile[each['name']]['all_networks'] = each['all_networks']
        port_profile[each['name']]['disabled'] = each['disabled']
        port_profile[each['name']]['duplex'] = each['duplex']
        port_profile[each['name']]['mac_limit'] = each['mac_limit']
        port_profile[each['name']]['mode'] = each['mode']
        port_profile[each['name']]['name'] = each['name']
        port_profile[each['name']]['networks'] = each['networks']
        port_profile[each['name']]['poe_disabled'] = each['poe_disabled']
        port_profile[each['name']]['port_auth'] = each['port_auth']
        port_profile[each['name']]['port_network'] = each['port_network']
        port_profile[each['name']]['speed'] = each['speed']
        port_profile[each['name']]['stp_edge'] = each['stp_edge']
        port_profile[each['name']]['voip_network'] = each['voip_network']
        mist_friendly_port_profiles.update(port_profile)

    switch_config['port_usages'] = mist_friendly_port_profiles

    # ### #################################################################################
    # ### # configuration push
    # ### #################################################################################
    if switch['provisioned'] is False:
        module.exit_json(changed=False, data='Device was not found, exiting')
    else:
        response = rest.put(f"/sites/{site_id}/devices/{switch['id']}", data=switch_config)
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
    argument_spec = MistHelper.mist_wired_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == '__main__':
    main()
