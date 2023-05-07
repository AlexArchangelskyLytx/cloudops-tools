#!/bin/bash

# example usage:

## check configs: ./fix_control_tower.sh
## delete configs: ./fix_control_tower.sh true

delete_mode=${1:-false}
delete_region=all

# Some configs have a non-default name
baseline_recorder_name="aws-controltower-BaselineConfigRecorder"
baseline_delivery_channel_name="aws-controltower-BaselineConfigDeliveryChannel"
default_recorder_name="default"
default_delivery_channel_name="default"

declare -a arr=("us-east-1" "us-east-2" "us-west-1" "us-west-2" "eu-central-1" "eu-north-1" "eu-west-1" "eu-west-2" "ap-south-1" "ap-southeast-1" "ap-southeast-2")

if [ "$delete_mode" = false ]; then
    for i in "${arr[@]}"; do
        echo "Scanning [$i]"
        aws --region "$i" configservice describe-configuration-recorders --output json --no-cli-pager
        aws --region "$i" configservice describe-delivery-channels --output json --no-cli-pager
    done
else
    echo "Delete mode enabled, will continue in three seconds."
    sleep 3
    if [ "$delete_region" = "all" ]; then
        for x in "${arr[@]}"; do
            echo "Deleting configuration for region [$x]"
            aws --region "$x" configservice delete-configuration-recorder --configuration-recorder-name "$baseline_recorder_name"
            aws --region "$x" configservice delete-configuration-recorder --configuration-recorder-name "$default_recorder_name"
            aws --region "$x" configservice delete-delivery-channel --delivery-channel-name "$baseline_delivery_channel_name"
            aws --region "$x" configservice delete-delivery-channel --delivery-channel-name "$default_delivery_channel_name"
            sleep 2
        done
    else
        aws --region $delete_region configservice delete-delivery-channel --delivery-channel-name "$baseline_delivery_channel_name"
        aws --region $delete_region configservice delete-delivery-channel --delivery-channel-name "$default_delivery_channel_name"
    fi
    echo "Done."
fi
