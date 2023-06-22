#!/usr/bin/env bash

# use with aws profiles generated with https://github.com/lytxinc/cloudops-tools/blob/main/infra/aws_config.py
# AWS_PROFILE needs to be payer - or run with aws-vault specifying the payer account
# This will build kubeconfig from EKS clusters discovered via AWS Config using the aggregator

build_kubeconfig() {

eks_instances=$(aws configservice select-aggregate-resource-config --configuration-aggregator-name aws-controltower-ConfigAggregatorForOrganizations --expression "SELECT accountId,resourceId,awsRegion WHERE resourceType='AWS::EKS::Cluster'" --output text |grep -v SELECTFIELDS |awk '{print $2}') 

for name in $eks_instances;do 
  accountId=$(echo "$name" |grep -v RESULTS|awk -F \" '{print $4}' )
  resourceId=$(echo "$name" |grep -v RESULTS |awk -F \" '{print $8}')
  region=$(echo "$name" |grep -v RESULTS|awk -F \" '{print $12}')
  for myaccount in $(echo -n "$accountId");
   do
     profiles=$(grep -C 3 "$myaccount" ~/.aws/config |grep profile |awk '{print $2}' |sed 's/]//g')
   done

aws eks update-kubeconfig --name "$resourceId" --kubeconfig ~/.kube/config --profile "$profiles" --region "$region"

done

}

build_kubeconfig;

