#!/bin/bash

# Set your AWS CLI profile if you have one configured
# If not, make sure you have the necessary IAM permissions to list SCPs
# aws configure --profile your-profile
#
get_root=$(aws organizations list-roots --query "Roots[0].Id" --output text)

# Get the list of OUs in the root of your AWS Organization
root_ou_id=$(aws organizations list-organizational-units-for-parent --parent-id $get_root --query "OrganizationalUnits[*].Id" --output text)
 

# List SCPs per OU in the root
for ou_id in $root_ou_id; do
    ou_name=$(aws organizations describe-organizational-unit --organizational-unit-id $ou_id --query "OrganizationalUnit.Name" --output text |grep .)
    echo "SCP list for OU: $ou_name ($ou_id)"
    aws organizations list-policies-for-target --target-id $ou_id --filter SERVICE_CONTROL_POLICY --query "Policies[*].Id" --output text |grep .
     echo ""
done

