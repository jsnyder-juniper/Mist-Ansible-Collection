#!/usr/bin/python

# Copyright: (c) 2020, Calvin Remsburg (@cremsburg) <cremsburg@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: mist_wlan

short_description: Manage lifecycle of WLANs within your Mist organization.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description: This module will leverage Mist's REST API to automate the lifecycle management of your WLANs in Mist.

options:
    airwatch:
        description:
            - airwatch settings
        required: false
        type: dict
        suboptions:
            enabled:
                required: false
                type: bool
            console_url:
                required: false
                type: str
            api_key:
                required: false
                type: str
            username:
                required: false
                type: str
            password:
                required: false
                type: str
    allow_mdns:
        description:
            - only applicable when limit_bcast==true
            - which allows mDNS / Bonjour packets to go through
            - default is false
        required: false
        type: bool
    allow_ipv6_ndp:
        description:
            - only applicable when limit_bcast==true
            - which allows or disallows ipv6 Neighbor Discovery packets to go through
            - default is true
        required: false
        type: bool
    ap_ids:
        description:
            - list of device ids
        required: false
        type: list
    api_token:
        description:
            - API token, used for authentication
            - can be stored as an environmental (MIST_API_KEY or MIST_API_TOKEN)
            - please consider using Ansible Vault or some other secure vault for this variable
        required: true
        type: str
    apply_to:
        description:
            - site / wxtags / aps
        required: false
        type: str
    arp_filter:
        description:
            - whether to enable smart arp filter
            - default is false
        required: false
        type: bool
    auth:
        description:
            - authentication/security policies
        required: false
        type: dict
        suboptions:
            type:
                description:
                    - open / psk / wep / eap / psk-tkip / psk-wpa2-tkip
                    - default is open
                required: false
                choices: ['open', 'psk', 'wep', 'eap', 'psk-tkip', 'psk-wpa2-tkip']
                type: str
            psk:
                description:
                    - when type=psk
                    - 8-64 characters
                    - 64 hex characters
                required: false
                type: str
            enable_mac_auth:
                description:
                    - whether to enable MAC Auth
                    - uses the same auth_servers
                    - default is false
                required: false
                type: bool
            multi_psk_only:
                description:
                    - whether to only use multi_psk
                    - default is false
                required: false
                type: bool
            private_wlan:
                description:
                    - whether private wlan is enabled.
                    - only applicable to multi_psk mode
                required: false
                type: bool
            keys:
                description:
                    - when type=wep
                    - four 10-character or 26-character hex string
                    - null can be used. 
                    - All keys, if provided, have to be in the same length
                required: false
                type: list
                elements: str
            key_idx:
                description:
                    - when type=wep
                    - 1 to 4
                    - default is 1
                required: false
                type: int
            eap_reauth:
                description:
                    - whether to trigger EAP reauth when the session ends
                    - default is false
                required: false
                type: bool
            pairwise:
                description:
                    - when type=psk / eap, pairwise needs to be declared as a list
                    - one of more of wpa2-ccmp / wpa1-tkip / wpa1-ccmp / wpa2-tkip
                    - default is [wpa2-ccmp]
                required: false
                type: list
                choices: ['wpa2-ccmp', 'wpa1-tkip', 'wpa1-ccmp', 'wpa2-tkip']
            wep_as_secondary_auth:
                description:
                    - enable WEP as secondary auth
                required: false
                type: bool
    auth_servers_nas_id:
        required: false
        type: str
    auth_servers_nas_ip:
        required: false
        type: str
    auth_servers_timeout:
        required: false
        type: int
    auth_servers_retries:
        required: false
        type: int
    auth_server_selection:
        required: false
        type: str
    auth_servers:
        required: false
        type: list
        elements: dict
        suboptions:
            host:
                required: false
                type: str
            port:
                required: false
                type: int
            secret:
                required: false
                type: str
    acct_servers:
        required: false
        type: list
        elements: dict
        suboptions:
            host:
                required: false
                type: str
            port:
                required: false
                type: int
            secret:
                required: false
                type: str
    acct_interim_interval:
        required: false
        type: int
    band:
        description:
            - which radio the wlan should apply to, both / 24 / 5
            - default is both
        required: false
        type: str
    band_steer:
        description:
            - whether to enable band_steering
            - this works only when band==both
            - default is false
        required: false
        type: bool
    band_steer_force_band5:
        description:
            - force dual-band capable client to connect to 5G
            - default is false
        required: false
        type: bool
    block_blacklist_clients:
        description:
            - whether to block the clients in the blacklist (up to first 256 macs)
        required: false
        type: bool
    cisco_cwa:
        required: false
        type: list
        elements: dict
        suboptions:
            enabled:
                required: false
                type: bool
            allowed_subnets:
                required: false
                type: list
                elements: str
            allowed_hostnames:
                required: false
                type: list
                elements: str
    client_limit_down_enabled:
        required: false
        type: bool
    client_limit_down:
        required: false
        type: int
    client_limit_up_enabled:
        required: false
        type: bool
    client_limit_up:
        required: false
        type: int
    coa_servers:
        required: false
        type: list
        elements: dict
        suboptions:
            enabled:
                required: false
                type: bool
            ip:
                required: false
                type: str
            port:
                required: false
                type: int
            secret:
                required: false
                type: str
            disable_event_timestamp_check:
                required: false
                type: bool
    disable_11ax:
        required: false
        type: bool
    disable_uapsd:
        required: false
        type: bool
    disable_wmm:
        required: false
        type: bool
    dtim:
        required: false
        type: int
    dynamic_psk:
        required: false
        type: bool
    dynamic_psk:
        description:
            - dynamic_psk allows PSK to be selected at runtime depending on context (wlan/site/user/...)
            - thus following configurations are assumed (currently)
            - PSK will come from RADIUS server
            - AP sends client MAC as username ans password (i.e. `enable_mac_auth` is assumed)
            - AP sends BSSID:SSID as Caller-Station-ID
            - `auth_servers` is required
            - `multi_psk_only` and `psk` is ignored
            - `pairwise` can only be wpa2-ccmp (for now, wpa3 support on the roadmap)
        required: false
        type: bool
    dynamic_vlan:
        required: false
        type: dict
        options:
            enabled:
                required: false
                type: bool
            type:
                required: false
                type: str
            port:
                required: false
                type: int
            vlans:
                required: false
                type: dict
                suboptions:
                    vlan:
                        required: false
                        type: str
                    name:
                        required: false
                        type: str
            default_vlan_id:
                required: false
                type: bool
            local_vlan_ids:
                required: false
                type: list
                elements: str
    enable_wireless_bridging:
        description:
            - whether to enable wireless bridging
            - which allows more broadcast packets to go through
        required: false
        type: bool
    enabled:
        description: 
            - determine if this wlan is enabled
            - default is True
        required: false
        type: bool
    hide_ssid:
        description:
            - whether to hide SSID in beacon
            - default is false
        required: false
        type: bool
    hostname_ie:
        required: false
        type: bool
    interface:
        required: false
        type: bool
    isolation:
        description:
            - whether to allow clients to talk to each other
            - default is false
        required: false
        type: bool
    legacy_overds:
        required: false
        type: bool
    level:
        description:
            - select if this WLAN applies to a site, an org, or something else
        required: false
        choices: ['org', 'site']
        type: str
    limit_bcast:
        description:
            - whether to list bcast (i.e. only allow certain bcast packets to go through)
            - default is false
        required: false
        type: bool
    limit_probe_response:
        required: false
        type: bool
    max_idletime:
        description:
            - max idle time in seconds
            - default is 1800
            - valid range is 60-86400
        required: false
        type: int
    mxtunnel_id:
        required: false
        type: str
    no_static_ip:
        description:
            - whether to only allow client that we've learned from DHCP exchange to talk
            - default is false
        required: false
        type: bool
    no_static_dns:
        description:
            - whether to only allow client to use DNS that we've learned from DHCP response
            - default is false
        required: false
        type: bool
    org_id:
        description:
            - your Mist Organization ID
            - can be found @ https://api.mist.com/api/v1/self
            - can leverage an environment of MIST_ORG_ID on your Ansible host
        required: true
        type: str
    radsec:
        required: false
        type: dict
        options:
            enabled:
                required: false
                type: bool
            server_name:
                required: false
                type: str
            servers:
                required: false
                type: list
                elements: dict
                suboptions:
                    host:
                        required: false
                        type: str
                    port:
                        required: false
                        type: int
            default_vlan_id:
                required: false
                type: int
            local_vlan_ids:
                required: false
                type: list
                elements: str
    roam_mode:
        description:
            - none (default) / OKC / 11r
        required: false
        type: str
    schedule:
        description:
            - WLAN operating schedule
        required: false
        type: dict
        suboptions:
            enabled:
                description:
                    - whether or not this schedule is enabled
                required: true
                type: bool
            hours:
                description:
                    - time ranges, the key is mon / tue / wed / thu / fri / sat / sun, the value is time range in HH:MM-HH:MM (24-hour format), the minimum resolution is 30 minute
                type: dict
                suboptions:
                    sun:
                        required: false
                        type: str
                    mon:
                        required: false
                        type: str
                    tue:
                        required: false
                        type: str
                    wed:
                        required: false
                        type: str
                    thu:
                        required: false
                        type: str
                    fri:
                        required: false
                        type: str
                    sat:
                        required: false
                        type: str
                    sun:
                        required: false
                        type: str
    sle_excluded:
        description:
            - whether to exclude this WLAN from SLE metrics
            - default is false
        required: false
        type: bool
    site_name:
        description:
            - for site-level WLANs only
            - name of the site
            - note: this is slower than using the site_id option
            -   it requires an additional API lookup to find the site_id
        required: false
        type: str
    site_id:
        description:
            - for site-level WLANs only
            - id of the site
            - note: this is slower than using the site_name option
            -   it requires an additional API lookup to find the site_id
        required: false
        type: str
    ssid:
        description: the name of the SSID
        required: false
        type: str
    state:
        description:
            - create or destroy this WLAN
        required: true
        choices: ['absent', 'present']
        type: str
    use_eapol_v1:
        required: true
        type: bool
    vlan_enabled:
        description:
            - if vlan tagging is enabled
            - default is false
        required: false
        type: bool
    vlan_id:
        description:
            - vlan id for wlan
        required: false
        type: int
    vlan_ids:
        description:
            - list of VLAN ids
        required: false
        type: list
        elements: int
    vlan_pooling:
        description:
            - vlan pooling allows AP to place client on different VLAN using a deterministic algorithm
            - default is false
        required: false
        type: bool
    wlan_limit_up_enabled:
        required: false
        type: bool
    wlan_limit_up:
        required: false
        type: int
    wlan_limit_down_enabled:
        required: false
        type: bool
    wlan_limit_down:
        required: false
        type: int
    wxtunnel_id:
        required: false
        type: str
    wxtunnel_remote_id:
        required: false
        type: str
    wxtag_ids:
        required: false
        type: list
        elements: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - cremsburg.mist.mist_wlan

author:
    - Calvin Remsburg (@cremsburg)
'''

EXAMPLES = r'''
### #################################################################
### # Create a site
### # assumes org_id and api_token are stored as environmentals
### # on the Ansible host, MIST_ORG_ID and MIST_API_KEY respectively
### #################################################################
- name: Create a new org-level WLAN
  cremsburg.mist.mist_wlan:
    ssid: "Yorke"
    level: "org"
    vlan_id: 15
    state: "present"

### #################################################################
### # Delete a site
### # here we will pass our org_id and api_token as variable
### # assumes you're storing these variables in some secrets Vault
### #################################################################
- name: Delete an existing site-level site
  cremsburg.mist.mist_wlan:
    ssid: "Yorke"
    level: "site"
    state: "absent"

### #################################################################
### # Create the whole enchilla of the wlan
### # passes org_id and api_token in plain text
### # please don't do this, protect your secrets
### #################################################################
- name: Create a new org-level WLAN
  cremsburg.mist.mist_wlan:
    ssid: "Yorke"
    enabled: true
    level: "org"
    vlan_id: 15
    auth:
        type: psk
        psk: juniper123
    band: both
    schedule:
        enabled: true
        hours:
            sun: "00:15-19:00"
            tue: "12:30-09:45"
    state: "present"
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

    # begin working on org-level WLANs
    if module.params['level'] == "org":

        # gather a list of wlans already created at the org-level
        response = rest.get(f"orgs/{org_id}/wlans")
        if response.status_code != 200:
            module.fail_json(msg=f"Failed to receive information about the current wlans, here is the response information to help you debug : {response.info}")

        # save the output of our API call to a new object called sites
        wlans = response.json

        # check to see if the wlans object is a list, fail the module if the return payload is anything else
        if isinstance(wlans, list):
            pass
        else:
            module.fail_json(msg=f"The wlans returned from the API are not in a list format, contant Mist support: {wlans}")

        # set a new variable to false, flip it to true if a site already matches the name. used later on for quitting early
        wlan = dict()
        wlan['provisioned'] = False
        wlan['id'] = None
        for each in wlans:
            if each['ssid'] == module.params['ssid']:
                wlan['provisioned'] = True
                wlan['id'] = each['id']

        # decide if it's appropriate to break out of the module based on our determination that the site does, or does not, exist
        if module.params['state'] == "absent":
            if wlan['provisioned'] is False:
                module.exit_json(changed=False, data="wlan does not exist, existing")
            else:
                response = rest.delete(f"/orgs/{org_id}/wlans/{wlan['id']}")
                module.exit_json(changed=True, data=response.json)

        elif module.params['state'] == "present":
            # create an empty dictionay
            wlan_data = dict()

            # set the key/value pairs of the parameters to a new object
            # iterate over the object, look to see if anything was entered
            # if there was something added by the user, append it to our empty dict
            parameters = module.params.items()
            for key, value in parameters:
                if value is not None:
                    wlan_data[key] = value

            if wlan['provisioned'] is False:
                response = rest.post(f"/orgs/{org_id}/wlans", data=wlan_data)
                module.exit_json(changed=True, data=response.json)
            else:
                response = rest.put(f"/orgs/{org_id}/wlans", data=wlan_data)
                module.exit_json(changed=True, data=response.json)

        else:
            module.exit_json(changed=False, data=response.json)

    # begin working on site-level WLANs
    elif module.params['level'] == "site":

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
                module.fail_json(msg=f"Failed to receive information about the current sites, here is the response information to help you debug : {response.info}")

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
                module.fail_json(msg=f"You selected a site level WLAN, but provided nothing for the site_id or site-name parameter. Be better : {response.info}")

            if site_id == "":
                module.fail_json(msg=f"You selected that does not exist. Here's the list we got back from Mist: {sites}")
        
        # gather a list of wlans already created at the org-level
        response = rest.get(f"sites/{site_id}/wlans")
        if response.status_code != 200:
            module.fail_json(msg=f"Failed to receive information about the current wlans, here is the response information to help you debug : {response.info}")

        # save the output of our API call to a new object called sites
        wlans = response.json

        # check to see if the wlans object is a list, fail the module if the return payload is anything else
        if isinstance(wlans, list):
            pass
        else:
            module.fail_json(msg=f"The wlans returned from the API are not in a list format, contant Mist support: {wlans}")

        # set a new variable to false, flip it to true if a site already matches the name. used later on for quitting early
        wlan = dict()
        wlan['provisioned'] = False
        wlan['id'] = None
        for each in wlans:
            if each['ssid'] == module.params['ssid']:
                wlan['provisioned'] = True
                wlan['id'] = each['id']

        # decide if it's appropriate to break out of the module based on our determination that the site does, or does not, exist
        if module.params['state'] == "absent":
            if wlan['provisioned'] is False:
                module.exit_json(changed=False, data="wlan does not exist, existing")
            else:
                response = rest.delete(f"/sites/{site_id}/wlans/{wlan['id']}")
                module.exit_json(changed=True, data=response.json)

        elif module.params['state'] == "present":
            # create an empty dictionay
            wlan_data = dict()

            # set the key/value pairs of the parameters to a new object
            # iterate over the object, look to see if anything was entered
            # if there was something added by the user, append it to our empty dict
            parameters = module.params.items()
            for key, value in parameters:
                if key == 'vlan_id':
                    if value is not None:
                        wlan_data['vlan_enabled'] = True
                if value is not None:
                    wlan_data[key] = value


            if wlan['provisioned'] is False:
                response = rest.post(f"/sites/{site_id}/wlans", data=wlan_data)
                module.exit_json(changed=True, data=response.json)
            else:
                response = rest.put(f"/sites/{site_id}/wlans/{wlan['id']}", data=wlan_data)
                module.exit_json(changed=True, data=response.json)

        else:
            module.exit_json(changed=False, data=response.json)


def main():
    # define the module's parameters
    argument_spec = MistHelper.mist_wlan_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == '__main__':
    main()
