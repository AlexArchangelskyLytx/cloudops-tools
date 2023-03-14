""" A script to automatically generate the ~/.aws/config file from the AWS orgs
API. This script requires an existing profile for the org account to be
configured for the first time.

NOTE: boto3 is required as a dependency.
"""

# Usage: aws-vault exec payer -- python aws_config.py

import os
import textwrap
from operator import itemgetter
from os.path import expanduser

import boto3

AWS_CONFIG = f"{expanduser('~')}/.aws/config"


def generate_config(accounts):
    # TODO: Create temporary config with access to org accounts if we don't have a config

    if os.path.isfile(AWS_CONFIG):
        os.rename(AWS_CONFIG, f"{AWS_CONFIG}.prev")

    # Recreate the config file
    with open(AWS_CONFIG, "w") as file:
        file.write(
            textwrap.dedent(
                """\
                [default]
                region = us-west-2
                output = json
                """
            )
        )

    # Create a template to generate the config from our json
    for account in accounts:
        # Sanitize account names
        account["Name"] = " ".join(
            account["Name"].replace(",", "").replace(" ", "-").lower().split()
        )

        account_profile = f"""\

        [profile {account["Name"].lower()}]
        sso_account_id = {account["Id"]}
        sso_region = us-west-2
        sso_role_name = AWSAdministratorAccess
        sso_start_url = https://d-92670a73b3.awsapps.com/start
        """

        with open(AWS_CONFIG, "a") as file:
            file.write(textwrap.dedent(account_profile))


def main():
    # Get all the accounts as json
    client = boto3.client("organizations")
    response = client.list_accounts()
    accounts = response["Accounts"]
    while "NextToken" in response:
        response = client.list_accounts(NextToken=response["NextToken"])
        accounts.extend(response["Accounts"])

    # Sort json for easier file navigation
    sorted_accounts = sorted(accounts, key=itemgetter("Name"))

    # Generate the resulting config
    generate_config(sorted_accounts)
    print("Done generating config")


if __name__ == "__main__":
    main()
