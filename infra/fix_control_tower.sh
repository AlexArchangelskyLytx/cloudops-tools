#!/bin/bash

delete_mode=${1:-false}
delete_region=all

# recorder_name="aws-controltower-BaselineConfigRecorder"
# delivery_channel_name="aws-controltower-BaselineConfigDeliveryChannel"
recorder_name="default"
delivery_channel_name="default"

declare -a arr=("us-east-1" "us-east-2" "us-west-1" "us-west-2" "eu-central-1" "eu-north-1" "eu-west-1" "eu-west-2" "ap-south-1" "ap-southeast-1" "ap-southeast-2")

if [ "$delete_mode" = false ]; then
    for i in "${arr[@]}"; do
        echo "Scanning [$i]"
        aws --region $i configservice describe-configuration-recorders --output json --no-cli-pager
        aws --region $i configservice describe-delivery-channels --output json --no-cli-pager
    done
else
    echo "Delete mode enabled, will continue in three seconds."
    sleep 3
    if [ "$delete_region" = "all" ]; then
        for x in "${arr[@]}"; do
            echo "Deleting configuration for region [$x]"
            aws --region $x configservice delete-configuration-recorder --configuration-recorder-name "$recorder_name"
            aws --region $x configservice delete-delivery-channel --delivery-channel-name "$delivery_channel_name"
            sleep 2
        done
    else
        aws --region $delete_region configservice delete-delivery-channel --delivery-channel-name "$delivery_channel_name"
    fi
    echo "Done."
fi
