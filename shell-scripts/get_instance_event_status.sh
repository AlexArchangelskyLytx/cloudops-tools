#!/usr/bin/env bash
#set -x

# This script assumes you have awscli_setup and you should have the following profiles in your ~/.aws/credentials file.
profiles=( micro-sbx network micro-prod )

for profile in "${profiles[@]}"
do

  if [ "$profile" = "micro-sbx" ]
  then

    # Check instances in us-west-2
    echo "Looking for scheduled events in $profile account..."
    instance_ids=$(aws ec2 describe-instance-status --profile "$profile" --region us-west-2 --query 'InstanceStatuses[?length(Events || `[]`) > `0`]' --output yaml | grep InstanceId | cut -d ':' -f 2 | sed -e 's/^[[:space:]]*//')

    if [ -z "$instance_ids" ]
    then
      echo "No scheduled events found."
      echo ""
    else
      echo "Found events scheduled for these instances:"
      while IFS= read -r instance_id
      do
        aws ec2 describe-instances --profile "$profile" --region us-west-2 --instance-id "$instance_id" --query "Reservations[*].Instances[*].Tags[?Key == 'Name']" --output yaml | grep Value
      done <<< "$instance_ids"
      echo ""
    fi

  else

    echo "Looking for scheduled events in $profile account..."
    instance_ids=$(aws ec2 describe-instance-status --profile "$profile" --query 'InstanceStatuses[?length(Events || `[]`) > `0`]' --output yaml | grep InstanceId | cut -d ':' -f 2 | sed -e 's/^[[:space:]]*//')

    if [ -z "$instance_ids" ]
    then
      echo "No scheduled events found."
      echo ""
    else
      echo "Found events scheduled for these instances:"
      while IFS= read -r instance_id
      do
        aws ec2 describe-instances --profile "$profile" --instance-id "$instance_id" --query "Reservations[*].Instances[*].Tags[?Key == 'Name']" --output yaml | grep Value
      done <<< "$instance_ids"
      echo ""
    fi

  fi
done
