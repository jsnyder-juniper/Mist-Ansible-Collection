=========================
cremsburg.mist.mist_wired
=========================

---------------------------------------------------------
Manage your Juniper EX switch configurations with Ansible
---------------------------------------------------------

mist_wired
================

This module will allow you to manage your Site Groups with Ansible. There is full documentation on the supported parameters within the module's source code, we'll try to point out interesting tidbits in this doc.

.. note::
   make sure you created environmentals on the ansible host that store your sensative info.
   in the case of this module, I am storing the following:

   - MIST_API_TOKEN
   - MIST_ORG_ID

   this prevents me from needing to declare a value for 'api_token' and 'org_id' in this module

Example
-------

Here is a basic example of using the module to configure your Site Groups

.. code-block:: yaml

    ---
    - hosts: localhost

      tasks:
        - name: configure a switch
          cremsburg.mist.mist_wired:
            name: Katy-SW1
            id: 00000000-0000-0000-1000-8403280bd289
            site_name: Katy
            oob_ip_config:
              type: dhcp
              network: default
            networks: 
              - name: home
                vlan_id: "91"
            port_config:
              - name: ge-0/0/0
                profile: mist-ap
            port_profiles:
              - name: mist-ap
                mode: trunk
                all_networks: True
                disabled: False
                port_network: "home"
                stp_edge: True
                poe_disabled: False

Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

    def mist_wired_spec():
        return dict(
            additional_config_cmds=dict(
                required=False,
                type='list',
                elements='str'),
            api_token=dict(
                required=True,
                fallback=(env_fallback, ['MIST_API_KEY', 'MIST_API_TOKEN']),
                no_log=True,
                type='str'),
            disable_auto_config=dict(
                required=False,
                type='bool'),
            id=dict(
                required=False,
                type='str'),
            ip_config=dict(
                required=False,
                type='dict',
                options=dict(
                    type=dict(
                        required=False,
                        type='str'),
                    network=dict(
                        required=False,
                        type='str'),
                    )
                ),
            mac=dict(
                required=False,
                type='str'),
            model=dict(
                required=False,
                type='str'),
            name=dict(
                required=True,
                type='str'),
            networks=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    name=dict(
                        required=False,
                        type='str'),
                    vlan_id=dict(
                        required=False,
                        type='str'),
                    ),
                ),
            notes=dict(
                required=False,
                type='str'),
            oob_ip_config=dict(
                required=False,
                type='dict',
                options=dict(
                    type=dict(
                        required=False,
                        type='str'),
                    network=dict(
                        required=False,
                        type='str'),
                    )
                ),
            org_id=dict(
                required=True,
                fallback=(env_fallback, ['MIST_ORG_ID']),
                type='str'),
            port_config=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    name=dict(
                        required=False,
                        type='str'),
                    profile=dict(
                        required=False,
                        type='str'),
                    ),
                ),
            port_profiles=dict(
                required=False,
                default=[],
                type='list',
                elements='dict',
                options=dict(
                    name=dict(
                        required=True,
                        type='str'),
                    all_networks=dict(
                        required=False,
                        type='bool'),
                    disabled=dict(
                        required=False,
                        type='bool'),
                    duplex=dict(
                        required=False,
                        type='str'),
                    mac_limit=dict(
                        required=False,
                        type='int'),
                    mode=dict(
                        required=False,
                        type='str'),
                    networks=dict(
                        required=False,
                        type='list'),
                    poe_disabled=dict(
                        required=False,
                        type='bool'),
                    port_auth=dict(
                        required=False,
                        type='str'),
                    port_network=dict(
                        required=False,
                        type='str'),
                    speed=dict(
                        required=False,
                        type='str'),
                    stp_edge=dict(
                        required=False,
                        type='bool'),
                    voip_network=dict(
                        required=False,
                        type='str'),
                    ),
                ),
            port_usages=dict(
                required=False,
                type='dict',
                options=dict(
                    name=dict(
                        required=False,
                        type='dict',
                        options=dict(
                            vlan_id=dict(
                                required=False,
                                type='str'),
                            )
                        ),
                    ),
                ),
            role=dict(
                required=False,
                type='str'),
            serial=dict(
                required=False,
                type='str'),
            site_id=dict(
                required=False,
                type='str'),
        )
