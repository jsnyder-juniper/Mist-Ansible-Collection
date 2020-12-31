==================================
cremsburg.mist.mist_site_groups
==================================

------------------------------------
Manage your Site Groups with Ansible
------------------------------------

mist_site_groups
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
        - name: create a Site Group
          cremsburg.mist.mist_site_groups:
              name: Retail
              state: present

The module is idempotent, so you can safely run this module even if the Site Group of Retail already exists. 

A seperate API call is made at runtime to gather a list of present Site Groups, and if there is a match between the Ansible module's 'name' parameter, and one of those found in the current list, the program will gracefully exit.

Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

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
