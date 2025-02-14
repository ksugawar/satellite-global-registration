# satellite-global-register.sh, satellite-global-register.py

## Purpose

This repository includes satellite-global-register.sh,
satellite-global-register.py, and roles/satellite_register_host that
are a shell script, a python script, and an ansible role,
respectively, and their purpose is to help you register a RHEL host to
Red Hat Satellite.

Traditionally, katello-consumer-ca-latest.noarch.rpm is downloaded
from the Satellite server and installed on the host, then
"subscription-manager register" command can be run on the host to
register it to the Satellite server. However, this method has been
deprecated for some time now, and the recommended method is the Global
Registration.

The Global Registration, if done by the book as described in Satellite
documentation, requires someone perform some Satellite Web UI
operations to generate a registration command that then has to be run
on the RHEL host to be registered, as opposed to the
katello-consumer-ca-latest method which was contained in operations on
the RHEL host in its entirety.

It is the main purpose of these scripts and ansible role to mitigate
this operational impact by containing the required operations in the
RHEL host, by letting the host access the Satellite API to acquire the
registration command dynamically generated by Satellite.

By using one of these scripts or the ansible role, the administrator
can now perform host registration without explicit operations on the
Satellite Web UI.

## License

Copyright (C) 2024, Ken Sugawara

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Support

Software distributed from this repository is not a product officially
supported by any person, group, or company.  Although the author will
make reasonable efforts to help users as the author's circumstances
permit, the author does not guarantee that any assistance will be
provided to users experiencing difficulties using the scripts or role
in a timely manner.

## Prerequisites

* There exists a Satellite user for registering hosts with "Register hosts" role only. (I strongly recommend against using Satellite admin user account for this purpose. It will expose admin password to unnecessarily large audience)
* There exist at least a content view, a life-cycle environment, an organization, and an activation key that connects all these resources (CV, LFE, and ORG) in the Satellite.
* The RHEL hosts to be registered, and ansible control host/execution node can connect by HTTP/HTTPS to the Satellite server (proxy is allowed)
* The RHEL host to be registered has standard Linux commands such as bash, python, curl, and sed already installed. It is confirmed that "Minimal" RHEL installation works in this regard.

## Usage of scripts

1. Edit satellite-global-register.sh and/or satellite-global-register.py and set appropriate values to the following four variables.

```
#### MINIMUM CONFIGURATION PARAMETERS
# REPLACE THESE VALUES WITH YOUR SATELLITE SERVER'S BEFORE DISTRIBUTING
sat_hostname='satellite.fqdn'
sat_username='username'
sat_password='password'
sat_activation_key='activation-key'
```


2. If necessary, edit any of the five variables contained in the section `#### Configurable Registration Parameters (Optional)`. If Satellite is to act simply as a private yum repository server, probably the default value will suffice.

```
#### Configurable Registration Parameters (Optional)
# insecure: true if Satellite server uses Self-Signed Certificate, False if not
insecure='true'
# insights: true if you want host to register to Red Hat Insights at registration time
insights='false'
# remote_exec: true if you plan to run commands on host from Satellite (requires ssh port open on host)
remote_exec='false'
# remote_exec_pull: true if you plan to run commands on host from Satellite in pull mode (does not require ssh port open on host; host subscribes to MQTT broker to receive remote execution job notifications)
remote_exec_pull='false'
```

NOTE: In case of satellite-global-register.py, boolean values should be capitalized True or False, without quotation marks.

3. Place the edited files satellite-global-register.sh and satellite-global-register.py to the Satellite server's /var/www/html/pub directory. Modify file permissions with `chmod` command for these files should be readable to all users.

4. When registering a host, run the following commands on the host itself as a privileged user (root).

RHEL 7 hosts:
```
curl -o satellite-global-register.sh http://satellite.fqdn/pub/satellite-global-register.sh
bash ./satellite-global-register.sh
```

RHEL 8/9 hosts:
```
curl -o satellite-global-register.py http://satellite.fqdn/pub/satellite-global-register.py
/usr/libexec/platform-python ./satellite-global-register.py
```

## Usage of Ansible role

See the sample playbook `sample-satellite-global-register.yml` for
usage. Required (mandatory) and optional configuration variables are
structured in a similar manner as the scripts, except that the
variable names start with the `satellite_reigster_` prefix:
```
# mandatory variables
satellite_register_hostname: 'satellite.example.com'
satellite_register_username: 'register'
satellite_register_password: 'changeme'
satellite_register_activation_key: 'default_activationkey'
# optional variables
satellite_register_dryrun: false
satellite_register_insecure: true
satellite_register_insights: false
satellite_register_remote_exec: false
satellite_register_remote_exec_pull: false
```

NOTE: The role fails to execute if any of mandatory variables are not defined.

Then, you can invoke the role as shown below:
```
  roles:
    - satellite_register_host
```
Or any other way you use to invoke a role within a playbook.
