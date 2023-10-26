#!/bin/bash

# Set your AWS region
AWS_REGION="us-west-2"

# Get a list of EC2 instance IDs that do not allow IMDSv1
IMDSv2_INSTANCE_IDS=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].InstanceId' --filters Name=metadata-options.http-tokens,Values=required --output text)
# Get a list of EC2 instance IDs that can allow IMDSv2
INSTANCE_IDS=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].InstanceId' --filters Name=metadata-options.http-tokens,Values=optional --output text)

echo "The following IDs already require tokens - IMDSv2 enabled"
echo "${IMDSv2_INSTANCE_IDS}"
echo ""

# Loop through the instance IDs
for INSTANCE_ID in $INSTANCE_IDS; do
  # Get the Metric data for MetadataNoToken
  METRIC_DATA=$(aws cloudwatch get-metric-data \
    --region "$AWS_REGION" \
    --metric-data-queries '[{"Id":"m1","MetricStat":{"Metric":{"Namespace":"AWS/EC2","MetricName":"MetadataNoToken","Dimensions":[{"Name":"InstanceId","Value":"'"$INSTANCE_ID"'"}]},"Period":300,"Stat":"Sum"},"ReturnData":true}]' \
    --start-time $(gdate -u +%Y-%m-%dT%H:%M:%SZ --date '-10950 hour') \
    --end-time $(gdate -u +%Y-%m-%dT%H:%M:%SZ) \
    --output json)

  # Extract the MetricValue (sum) from the MetricDataResults
  METRIC_VALUE=$(echo  "$METRIC_DATA" | jq -r '.MetricDataResults[0].Values[]' |gpaste -sd+ |bc)
  #echo $METRIC_VALUE

  # Determine if IMDSv2 is enabled or not
  if [ "$METRIC_VALUE" == 0 ]; then
    IMDS_STATUS="IMDSv2 can be enabled"
  elif [ -z "$METRIC_VALUE" ]; then
    IMDS_STATUS="No metric data - host probably offline, need to validate"
  else
    IMDS_STATUS="IMDSv2 can't be enabled"
  fi

  # Print the result
  echo "Instance ID: $INSTANCE_ID - $IMDS_STATUS"
done

