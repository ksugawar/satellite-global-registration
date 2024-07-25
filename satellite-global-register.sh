#!/bin/bash

#### MINIMUM CONFIGURATION PARAMETERS
# REPLACE THESE VALUES WITH YOUR SATELLITE SERVER'S BEFORE DISTRIBUTING
sat_hostname='satellite.fqdn'
sat_username='username'
sat_password='password'
sat_activation_key='activation-key'

#### Configurable Registration Parameters (Optional)
# insecure: true if Satellite server uses Self-Signed Certificate, False if not
insecure='true'
# insights: true if you want host to register to Red Hat Insights at registration time
insights='false'
# remote_exec: true if you plan to run commands on host from Satellite (requires ssh port open on host)
remote_exec='false'
# remote_exec_pull: true if you plan to run commands on host from Satellite in pull mode (does not require ssh port open on host; host subscribes to MQTT broker to receive remote execution job notifications)
remote_exec_pull='false'

URL="https://${sat_hostname}/api/registration_commands"
PAYLOAD='{ "registration_command": { "activation_keys": ["'${sat_activation_key}'"], "insecure": '${insecure}', "setup_insights": '${insights}', "setup_remote_execution": '${remote_exec}', "setup_remote_execution_pull": '${remote_exec_pull}' }}'

RESPONSE=$(curl -k -X POST "${URL}" \
  --user "${sat_username}:${sat_password}" -H 'Content-Type: application/json' -d "${PAYLOAD}" )

# echo "${RESPONSE}" | od -c

REG_CMDLINE=$(echo ${RESPONSE} |
  sed -e 's/^.*"registration_command":"\([^"]*\)".*$/\1/' -e 's/\\u0026/\&/g')

echo "${REG_CMDLINE}"
eval "${REG_CMDLINE}"
