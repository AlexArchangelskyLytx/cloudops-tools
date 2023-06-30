#!/usr/bin/env bash

# AWS_PROFILE needs to be payer - or run with aws-vault specifying the payer account
# This will build a AWS config file named my_config, this has the profile set as the account id

accounts=$(aws organizations list-accounts --output text |awk '{print $4}')
touch my_config

echo "[default]
region = us-west-2
output = json

[sso-session Lytx]
sso_start_url = https://d-92670a73b3.awsapps.com/start#/
sso_region = us-west-2
sso_registration_scopes = sso:account:access
" >> my_config

for name in $accounts;do

echo "[profile $name]
sso_account_id = $name
sso_session = Lytx
sso_region = us-west-2
sso_role_name = AWSAdministratorAccess
" >> my_config;

done
