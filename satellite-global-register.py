#!/usr/libexec/platform-python
# Tested on RHEL 8 (Python 3.6) and RHEL 9 (Python 3.9)
# Tested but failed on RHEL 7 (Python 2.7)

import json
import subprocess

#### MINIMUM CONFIGURATION PARAMETERS
# REPLACE THESE VALUES WITH YOUR SATELLITE SERVER'S BEFORE DISTRIBUTING
sat_hostname='satellite.fqdn'
sat_username='username'
sat_password='password'
sat_activation_key='activation-key'

#### Configurable Registration Parameters (Optional)
# insecure: True if Satellite server uses Self-Signed Certificate, False if not
insecure=True
# insights: True if you want host to register to Red Hat Insights at registration time
insights=False
# remote_exec: True if you plan to run commands on host from Satellite (requires ssh port open on host)
remote_exec=False
# remote_exec_pull: True if you plan to run commands on host from Satellite in pull mode (does not require ssh port open on host; host subscribes to MQTT broker to receive remote execution job notifications)
remote_exec_pull=False

url='https://{}/api/registration_commands'.format(sat_hostname)
payload={ "registration_command": { "activation_keys": [ sat_activation_key ], "insecure": insecure, "setup_insights": insights, "setup_remote_execution": remote_exec, "setup_remote_execution_pull": remote_exec_pull } }

result = subprocess.run([ 'curl', '-k', '-X', 'POST', url, '--user', '{}:{}'.format(sat_username,sat_password), '-H', 'Content-Type: application/json', '-d', json.dumps(payload) ], stdout=subprocess.PIPE)

if (result.returncode == 0):
    # success
    reply = json.loads(result.stdout)
    registration_command = reply["registration_command"]
    print(registration_command)
    subprocess.run(['bash', '-c', registration_command])
else:
    # failure
    print('Failed to obtain registration command via Satellite API: {}'.format(result.stderr))
