# Juniper Mist Ansible Modules

[![N|Solid](https://github.com/cremsburg/Mist-Ansible-Collection/static/images/Mist-Juniper-Logo-Full-Color.svg)](https://www.mist.com/)

[![Build Status](https://api.travis-ci.com/cremsburg/Mist-Ansible-Collection.svg?branch=main)](https://travis-ci.com/github/cremsburg/Mist-Ansible-Collection)

## `Overview`

The goal of this collection is to provide an easier way to interact with Juniper Mist. While nothing will stop you from using the built-in module, you may find that working with pre-packaged modules can help simplify the development of your playbook, or it may just be easier to support as a team.

## 📋 `Ansible version compatibility`

There are significant changes to Ansible within version 2.10.x, and while those changes get worked out we will continue to test for Ansible 2.9.x.

It is very likely that something will break on Ansible 2.10.x versions as of this pre-release version of the project.

## ⚙️ `Batteries Included`

Here is a short list of modules included within the collection, expect feature parity with the [official Postman collection](https://documenter.getpostman.com/view/224925/SzYgQufe?version=latest#intro) before this project hits `version 0.1.0`

Name | Description
---- | -----------
[cremsburg.mist.mist_site](https://github.com/cremsburg/mist_ansible_modules/blob/main/cremsburg/mist/docs/cremsburg.mist.mist_site.rst)|Manage the lifecycle of a site
[cremsburg.mist.mist_site_groups](https://github.com/cremsburg/mist_ansible_modules/blob/main/cremsburg/mist/docs/cremsburg.mist.mist_site_groups.rst)|Manage the Site Groups of your organization
[cremsburg.mist.mist_wlan](https://github.com/cremsburg/mist_ansible_modules/blob/main/cremsburg/mist/docs/cremsburg.mist.mist_wlan.rst)|Manage the lifecycle of a WLAN

## 🚀 `Executing the playbook`

After installing the collections, you can call the modules by using their full name path.

`test.yaml`

```yaml
---
- hosts: localhost

  ### ####################################################
  ### # make sure you created environmentals on the
  ### #   ansible host that store your sensative info
  ### #   in this case, i am using the following
  ### #     - MIST_API_TOKEN
  ### #     - MIST_ORG_ID
  ### #   this prevents me from needing to declare a value
  ### #   for 'api_token' and 'org_id' in this module
  ### ####################################################
  tasks:
    - name: create a site
      cremsburg.mist.mist_site:
        name: katy
        address: 5000 Katy Mills Cir, Katy, TX 77494, USA
        country_code: test_project
        latlng: 
          lat: 29.7785301
          lng: -95.8154901
        notes: this is a test
        state: present

```

Then simply run your playbook

```sh
ansible-playbook test.yaml
```

If you used Ansible Vault to encrypt your secrets, you need to append the `--ask-vault-pass` to your command.

## ⚠️ Very Important! ⚠️

Please make sure to manage your sensative information carfully. While the modules support the parameter of `api_key`, this should never be statically entered with your token in clear text.

Here are better alternatives:

### Manage your API token as an environmental

```sh
export MIST_API_TOKEN='YOUR_PRIVATE_KEY_HERE'
```

> you can also use `MIST_API_KEY`, if you prefer

### Manage your API token as a secret with Ansible Vault

create a file to store your API token in

`$ vim vault.yaml`

```yaml
api_token: "MY_MIST_API_TOKEN_HERE"
```

encrypt the new file

```sh
ansible-vault encrypt vault.yml
```

update your playbook to look for variables within this new, encrypted file

```yaml
---
- hosts: localhost
  vars_files:
    - vault.yml
  tasks:
    - name: create a site
      cremsburg.mist.mist_site:
        name: katy
        address: 5000 Katy Mills Cir, Katy, TX 77494, USA
        country_code: test_project
        latlng: 
          lat: 29.7785301
          lng: -95.8154901
        notes: this is a test
        api_token: "{{ api_token }}"
        state: present

```

and now you'll need to pass your vault password when using the playbook

```sh
ansible-playbook --ask-vault-pass test.yaml
```

## Development

Want to contribute? Great!

Submit a PR and let's work on this together :D
