#!/usr/bin/env bash

## Instructions for connecting to EC2 instances without SSH keys

# Install session manager
# https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html

# Start a session
# https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-sessions-start.html

# aws ssm start-session --target i-001234a4bf70dec41EXAMPLE

# Install instance-connect
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-set-up.html

# pip install ec2instanceconnectcli

# Connect to an instance
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-methods.html

# mssh i-001234a4bf70dec41EXAMPLE
