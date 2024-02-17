#!/usr/bin/env bash

main() {
  # Get the list of all AWS accounts
  aws_accounts=$(aws-vault list | awk '{print $1}' | grep cloudinfra)
  stack="SECOPS-AWSCloudFormationStackSetExecutionRole-Stack"

  for account in $aws_accounts; do
    stack=$(aws-vault exec "$account" -- aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --query "StackSummaries[?StackName=='SECOPS-AWSCloudFormationStackSetExecutionRole-Stack'].StackName" --output text)

    # Check if the stack is an empty string
    if [[ -z "$stack" ]]; then
      echo "Stack doesn't exist in account ${account%%/*}, skipping delete"
      continue
    fi

    # Skip delete if dry-run flag is passed
    if [[ $1 == "--delete" ]]; then
      echo "Deleting '$stack' stack in account ${account%%/*}"
      aws-vault exec "$account" -- aws cloudformation delete-stack --stack-name "$stack"
    else
      echo "Dry run, skipping delete"
      echo "Account: ${account%%/*}, Stack name: $stack"
      aws-vault exec "$account" -- aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --query "StackSummaries[?StackName=='SECOPS-AWSCloudFormationStackSetExecutionRole-Stack'].StackName" --output text
    fi
  done
}

main "$@"
