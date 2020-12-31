===========================
cremsburg.mist.mist_site
===========================

------------------------------
Manage your sites with Ansible
------------------------------

mist_site
=========

This module will allow you to manage your sites with Ansible. There is full documentation on the supported parameters within the module's source code

.. note::
   make sure you created environmentals on the ansible host that store your sensative info.
   in the case of this module, I am storing the following:

   - MIST_API_TOKEN
   - MIST_ORG_ID

   this prevents me from needing to declare a value for 'api_token' and 'org_id' in this module


Example
-------

Here is a basic example of using the module to configure your site

.. code-block:: yaml

    ---
    - hosts: localhost

      tasks:
        - name: create a site
          cremsburg.mist.mist_site:
              name: katy
              address: 5000 Katy Mills Cir, Katy, TX 77494, USA
              country_code: US
              sitegroups:
                - "iot"
              latlng:
                lat: 29.7785301
                lng: -95.8154901
              notes: this is a test
              state: present

Here is an example of using the module to add or remove Site Group associations to a site.

.. warning::
   This is declartive, meaning that a site will only have the Site Groups associated to it that are listed here.


.. code-block:: yaml

    ---
    - hosts: localhost

      tasks:
        - name: create a site
          cremsburg.mist.mist_site:
              name: katy
              sitegroups:
                - "retail"
                - "corporate"
              state: present

The module is idempotent, so you can safely run this module even if the Site Group of Retail already exists. 

A seperate API call is made at runtime to gather a list of present Sites, and if there is a match between the Ansible module's 'name' parameter, and one of those found in the current list, the program will gracefully exit.

Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

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
