# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Calvin Remsburg (@cremsburg) <cremsburg@protonmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_text
from ansible.module_utils.basic import env_fallback


class Response(object):

    def __init__(self, resp, info):
        self.body = None
        if resp:
            self.body = resp.read()
        self.info = info

    @property
    def json(self):
        if not self.body:
            if "body" in self.info:
                return json.loads(to_text(self.info["body"]))
            return None
        try:
            return json.loads(to_text(self.body))
        except ValueError:
            return None

    @property
    def status_code(self):
        return self.info["status"]


class MistHelper:

    def __init__(self, module):
        self.module = module
        self.baseurl = 'https://api.mist.com/api/v1'
        self.timeout = module.params.get('timeout', 30)
        self.api_token = module.params.get('api_token')
        self.headers = {'Authorization': f'Token {self.api_token}',
                        'Content-type': 'application/json'}

        # Check if api_token is valid or not
        response = self.get('self')
        if response.status_code == 401:
            self.module.fail_json(msg='Failed to login using API token, please verify validity of API token.')

    def _url_builder(self, path):
        if path[0] == '/':
            path = path[1:]
        return f'{self.baseurl}/{path}'

    def send(self, method, path, data=None):
        url = self._url_builder(path)
        data = self.module.jsonify(data)

        resp, info = fetch_url(self.module,
                               url,
                               data=data,
                               headers=self.headers,
                               method=method,
                               timeout=self.timeout)

        return Response(resp, info)

    def get(self, path, data=None):
        return self.send('GET', path, data)

    def put(self, path, data=None):
        return self.send('PUT', path, data)

    def post(self, path, data=None):
        return self.send('POST', path, data)

    def delete(self, path, data=None):
        return self.send('DELETE', path, data)

    @staticmethod
    def mist_site_spec():
        return dict(
            address=dict(
                required=False,
                type='str'),
            alarmtemplate_id=dict(
                required=False,
                type='str'),
            api_token=dict(
                required=True,
                fallback=(env_fallback, ['MIST_API_KEY', 'MIST_API_TOKEN']),
                no_log=True,
                type='str'),
            country_code=dict(
                required=False,
                type='str'),
            latlng=dict(
                required=False,
                type='dict',
                options=dict(
                    lat=dict(
                        required=False,
                        type='float'),
                    lng=dict(
                        required=False,
                        type='float'),
                    )
                ),
            name=dict(
                required=False,
                type='str'),
            notes=dict(
                required=False,
                type='str'),
            org_id=dict(
                required=True,
                fallback=(env_fallback, ['MIST_ORG_ID']),
                type='str'),
            rftemplate_id=dict(
                required=False,
                type='str'),
            secpolicy_id=dict(
                required=False,
                type='str'),
            sitegroups=dict(
                required=False,
                type='list',
                elements='str'),
            state=dict(
                required=True,
                choices=['present', 'absent'],
                type='str'),
            timeout=dict(
                required=False,
                type='int'),
            timezone=dict(
                required=False,
                type='str'),
            validate_certs=dict(
                type='bool',
                required=False),
        )

    @staticmethod
    def mist_site_groups_spec():
        return dict(
            api_token=dict(
                required=True,
                fallback=(env_fallback, ['MIST_API_KEY', 'MIST_API_TOKEN']),
                no_log=True,
                type='str'),
            name=dict(
                required=True,
                type='str'),
            org_id=dict(
                required=True,
                fallback=(env_fallback, ['MIST_ORG_ID']),
                type='str'),
            site_ids=dict(
                required=False,
                type='list',
                elements='str'),
            state=dict(
                required=True,
                type='str'),
        )

    @staticmethod
    def mist_wlan_spec():
        return dict(
            airwatch=dict(
                required=False,
                type='dict',
                options=dict(
                    enabled=dict(
                        required=False,
                        type='bool'),
                    console_url=dict(
                        required=False,
                        type='str'),
                    api_key=dict(
                        required=False,
                        type='str'),
                    username=dict(
                        required=False,
                        type='str'),
                    password=dict(
                        required=False,
                        type='str'),
                    ),
                ),
            allow_mdns=dict(
                required=False,
                default=False,
                type='bool'),
            allow_ipv6_ndp=dict(
                required=False,
                type='bool'),
            ap_ids=dict(
                required=False,
                type='list',
                elements='str'),
            api_token=dict(
                required=True,
                fallback=(env_fallback, ['MIST_API_KEY', 'MIST_API_TOKEN']),
                no_log=True,
                type='str'),
            apply_to=dict(
                required=False,
                type='str'),
            arp_filter=dict(
                required=False,
                type='bool'),
            auth=dict(
                required=False,
                type='dict',
                options=dict(
                    type=dict(
                        required=False,
                        choices=['open', 'psk', 'wep', 'eap', 'psk-tkip', 'psk-wpa2-tkip'],
                        type='str'),
                    psk=dict(
                        required=False,
                        type='str'),
                    enable_mac_auth=dict(
                        required=False,
                        type='bool'),
                    multi_psk_only=dict(
                        required=False,
                        type='bool'),
                    pairwise=dict(
                        required=False,
                        type='list',
                        elements='str'),
                    wep_as_secondary_auth=dict(
                        required=False,
                        type='bool'),
                    private_wlan=dict(
                        required=False,
                        type='bool'),
                    keys=dict(
                        required=False,
                        type='list',
                        elements='str'),
                    key_idx=dict(
                        required=False,
                        type='int'),
                    eap_reauth=dict(
                        required=False,
                        type='bool'),
                    ),
                ),
            auth_servers_nas_id=dict(
                required=False,
                type='str'),
            auth_servers_nas_ip=dict(
                required=False,
                type='str'),
            auth_servers_timeout=dict(
                required=False,
                type='int'),
            auth_servers_retries=dict(
                required=False,
                type='int'),
            auth_server_selection=dict(
                required=False,
                type='str'),
            auth_servers=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    host=dict(
                        required=False,
                        type='str'),
                    port=dict(
                        required=False,
                        type='int'),
                    secret=dict(
                        required=False,
                        type='str'),
                    ),
                ),
            acct_servers=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    host=dict(
                        required=False,
                        type='str'),
                    port=dict(
                        required=False,
                        type='int'),
                    secret=dict(
                        required=False,
                        type='str'),
                    ),
                ),
            acct_interim_interval=dict(
                required=False,
                type='int'),
            band=dict(
                required=False,
                type='str'),
            band_steer=dict(
                required=False,
                type='bool'),
            band_steer_force_band5=dict(
                required=False,
                type='bool'),
            block_blacklist_clients=dict(
                required=False,
                type='bool'),
            cisco_cwa=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    enabled=dict(
                        required=False,
                        type='bool'),
                    allowed_subnets=dict(
                        required=False,
                        type='list',
                        elements='str'),
                    allowed_hostnames=dict(
                        required=False,
                        type='list',
                        elements='str'),
                    ),
                ),
            client_limit_down_enabled=dict(
                required=False,
                type='bool'),
            client_limit_down=dict(
                required=False,
                type='int'),
            client_limit_up_enabled=dict(
                required=False,
                type='bool'),
            client_limit_up=dict(
                required=False,
                type='int'),
            coa_servers=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    enabled=dict(
                        required=False,
                        type='bool'),
                    ip=dict(
                        required=False,
                        type='str'),
                    port=dict(
                        required=False,
                        type='int'),
                    secret=dict(
                        required=False,
                        type='str'),
                    disable_event_timestamp_check=dict(
                        required=False,
                        type='bool'),
                    ),
                ),
            disable_11ax=dict(
                required=False,
                type='bool'),
            disable_uapsd=dict(
                required=False,
                type='bool'),
            disable_wmm=dict(
                required=False,
                type='bool'),
            dtim=dict(
                required=False,
                type='int'),
            dynamic_psk=dict(
                required=False,
                type='bool'),
            dynamic_vlan=dict(
                required=False,
                type='dict',
                options=dict(
                    enabled=dict(
                        required=False,
                        type='bool'),
                    type=dict(
                        required=False,
                        type='str'),
                    vlans=dict(
                        required=False,
                        type='dict',
                        options=dict(
                            vlan=dict(
                                required=False,
                                type='str'),
                            name=dict(
                                required=False,
                                type='str'),
                            )
                        ),
                    default_vlan_id=dict(
                        required=False,
                        type='int'),
                    local_vlan_ids=dict(
                        required=False,
                        type='list',
                        elements='str'),
                    ),
                ),
            enable_wireless_bridging=dict(
                required=False,
                type='bool'),
            enabled=dict(
                required=False,
                type='bool'),
            hide_ssid=dict(
                required=False,
                type='bool'),
            hostname_ie=dict(
                required=False,
                type='bool'),
            interface=dict(
                required=False,
                type='str'),
            isolation=dict(
                required=False,
                type='bool'),
            legacy_overds=dict(
                required=False,
                type='bool'),
            level=dict(
                required=False,
                choices=['org', 'site'],
                type='str'),
            limit_bcast=dict(
                required=False,
                type='bool'),
            limit_probe_response=dict(
                required=False,
                type='bool'),
            max_idletime=dict(
                required=False,
                type='int'),
            mxtunnel_id=dict(
                required=False,
                type='str'),
            no_static_ip=dict(
                required=False,
                type='bool'),
            no_static_dns=dict(
                required=False,
                type='bool'),
            org_id=dict(
                required=True,
                fallback=(env_fallback, ['MIST_ORG_ID']),
                type='str'),
            radsec=dict(
                required=False,
                type='dict',
                options=dict(
                    enabled=dict(
                        required=False,
                        type='bool'),
                    server_name=dict(
                        required=False,
                        type='str'),
                    servers=dict(
                        required=False,
                        type='list',
                        elements='dict',
                        options=dict(
                            host=dict(
                                required=False,
                                type='str'),
                            port=dict(
                                required=False,
                                type='int'),
                            )
                        ),
                    default_vlan_id=dict(
                        required=False,
                        type='int'),
                    local_vlan_ids=dict(
                        required=False,
                        type='list',
                        elements='str'),
                    ),
                ),
            rateset=dict(
                required=False,
                type='dict',
                options=dict(
                    # got to find a way to use the k/v used by mist api.
                    #   can't believe it, but they're using integers as keys
                    #   this won't work right away
                    twentyfour=dict(
                        required=False,
                        type='dict',
                        options=dict(
                            min_rssi=dict(
                                required=False,
                                type='int'),
                            template=dict(
                                required=False,
                                type='str'),
                            legacy=dict(
                                required=False,
                                type='list',
                                elements='str'),
                            ht=dict(
                                required=False,
                                type='str'),
                            )
                        ),
                    five=dict(
                        required=False,
                        type='dict',
                        options=dict(
                            min_rssi=dict(
                                required=False,
                                type='int'),
                            template=dict(
                                required=False,
                                type='str'),
                            legacy=dict(
                                required=False,
                                type='list',
                                elements='str'),
                            ht=dict(
                                required=False,
                                type='str'),
                            vht=dict(
                                required=False,
                                type='str'),
                            )
                        ),
                    default_vlan_id=dict(
                        required=False,
                        type='int'),
                    local_vlan_ids=dict(
                        required=False,
                        type='list',
                        elements='str'),
                    ),
                ),
            roam_mode=dict(
                required=False,
                type='str'),
            schedule=dict(
                required=False,
                type='dict',
                options=dict(
                    enabled=dict(
                        required=False,
                        type='bool'),
                    hours=dict(
                        required=False,
                        type='dict',
                        options=dict(
                            sun=dict(
                                required=False,
                                type='str'),
                            mon=dict(
                                required=False,
                                type='str'),
                            tue=dict(
                                required=False,
                                type='str'),
                            wed=dict(
                                required=False,
                                type='str'),
                            thr=dict(
                                required=False,
                                type='str'),
                            fri=dict(
                                required=False,
                                type='str'),
                            sat=dict(
                                required=False,
                                type='str'),
                            ),
                        ),
                    )
                ),
            sle_excluded=dict(
                required=False,
                type='bool'),
            site_name=dict(
                required=False,
                type='str'),
            site_id=dict(
                required=False,
                type='str'),
            ssid=dict(
                required=False,
                type='str'),
            state=dict(
                required=False,
                choices=['absent', 'present'],
                type='str'),
            use_eapol_v1=dict(
                required=False,
                type='bool'),
            vlan_enabled=dict(
                required=False,
                type='bool'),
            vlan_id=dict(
                required=False,
                type='int'),
            vlan_pooling=dict(
                required=False,
                type='bool'),
            vlan_ids=dict(
                required=False,
                type='list',
                elements='str'),
            wlan_limit_up_enabled=dict(
                required=False,
                type='bool'),
            wlan_limit_up=dict(
                required=False,
                type='int'),
            wlan_limit_down_enabled=dict(
                required=False,
                type='bool'),
            wlan_limit_down=dict(
                required=False,
                type='int'),
            wxtunnel_id=dict(
                required=False,
                type='str'),
            wxtunnel_remote_id=dict(
                required=False,
                type='str'),
            wxtag_ids=dict(
                required=False,
                type='list',
                elements='str'),
        )
