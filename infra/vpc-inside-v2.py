# To run this script obtain SSO token first e.g:
# aws sso login --profile 069442728920

import logging
import boto3
from argparse import ArgumentParser, HelpFormatter
from botocore.exceptions import ClientError, ProfileNotFound

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(message)s')

# Argument parser config
formatter = lambda prog: HelpFormatter(prog, max_help_position=52)
parser = ArgumentParser(formatter_class=formatter)
# parser = ArgumentParser()
parser.add_argument("-v", "--vpc", required=True, help="The VPC to describe")
parser.add_argument("-r", "--region", default="us-east-1", help="AWS region that the VPC resides in")
parser.add_argument("-p", '--profile', default='default', help="AWS profile")
args = parser.parse_args()

# boto client config
try:
    session = boto3.Session(profile_name=args.profile)
except ProfileNotFound as e:
    logger.warning("{}, please provide a valid AWS profile name".format(e))
    exit(-1)

vpc_client = session.client("ec2", region_name=args.region)
elbV2_client = session.client('elbv2', region_name=args.region)
elb_client = session.client('elb', region_name=args.region)
lambda_client = session.client('lambda', region_name=args.region)
eks_client = session.client('eks', region_name=args.region)
asg_client = session.client('autoscaling', region_name=args.region)
rds_client = session.client('rds', region_name=args.region)
ec2 = session.resource('ec2', region_name=args.region)

vpc_id: str = args.vpc


def vpc_in_region():
    vpc_exists = False
    try:
        vpcs = list(ec2.vpcs.filter(Filters=[]))
    except ClientError as e:
        logger.warning(e.response['Error']['Message'])
        exit()
    logger.info("VPCs in region {}:".format(args.region))
    counter = 0
    for vpc in vpcs:
        logger.info(vpc.id)
        counter += 1
        if vpc.id == vpc_id:
            vpc_exists = True
            
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return vpc_exists

#### START

def describe_igws():
    igws = vpc_client.describe_internet_gateways(
        Filters=[{"Name": "attachment.vpc-id",
                  "Values": [vpc_id]}])['InternetGateways']
    # print(igws)
    igws = [igw['InternetGatewayId'] for igw in igws]

    logger.info("Internet Gateways in VPC {}:".format(vpc_id))
    
    counter = 0
    for igw in igws:
        cigw = f'\033[31m{igw}\033[00m'
        logger.info(cigw)
        counter += 1
    logger.info(f'\033[31mTotal: {counter}\033[00m')
    logger.info("--------------------------------------------")
    return


def describe_vpc_peering_connections_accepter():
    pconns = vpc_client.describe_vpc_peering_connections(
        # Filters=[{"Name": "accepter-vpc-info.vpc-id",
        Filters=[{"Name": "requester-vpc-info.vpc-id",
                  "Values": [vpc_id]}])['VpcPeeringConnections']
    
    # print(pconns)
    
    # pconns = [pconn['RequesterVpcInfo']['VpcId'] for pconn in pconns]
    pconns = [pconn['AccepterVpcInfo']['VpcId'] for pconn in pconns]
    
    logger.info("Peering Connections Accepter in VPC {}:".format(vpc_id))
    
    counter = 0
    for pconn in pconns:
        cpconn = f'\033[31m{pconn}\033[00m'
        logger.info(cpconn)
        counter += 1
    logger.info(f'\033[31mTotal: {counter}\033[00m')
    logger.info("--------------------------------------------")
    return


def describe_vpc_peering_connections_requester():
    pconns = vpc_client.describe_vpc_peering_connections(
        Filters=[{"Name": "accepter-vpc-info.vpc-id",
        # Filters=[{"Name": "requester-vpc-info.vpc-id",
                  "Values": [vpc_id]}])['VpcPeeringConnections']
    
    # print(pconns)
    
    pconns = [pconn['RequesterVpcInfo']['VpcId'] for pconn in pconns]
    # pconns = [pconn['AccepterVpcInfo']['VpcId'] for pconn in pconns]
    
    logger.info("Peering Connections Requester in VPC {}:".format(vpc_id))
    
    counter = 0
    for pconn in pconns:
        cpconn = f'\033[31m{pconn}\033[00m'
        logger.info(cpconn)
        counter += 1
    logger.info(f'\033[31mTotal: {counter}\033[00m')
    logger.info("--------------------------------------------")
    return


def describe_nats():
    nats = vpc_client.describe_nat_gateways(Filters=[{"Name": "vpc-id",
                                                      "Values": [vpc_id]}])['NatGateways']

    nats = [nat['NatGatewayId'] for nat in nats]
    logger.info("NAT Gateways in VPC {}:".format(vpc_id))
    counter = 0
    for nat in nats:
        cnat = f'\033[31m{nat}\033[00m'
        logger.info(cnat)
        counter += 1
    logger.info(f'\033[31mTotal: {counter}\033[00m')
    logger.info("--------------------------------------------")
    return



def describe_tgwas():
    tgwas = vpc_client.describe_transit_gateway_attachments(Filters=[{"Name": "resource-id",
                                                      "Values": [vpc_id]}])['TransitGatewayAttachments']

    tgwas = [tgwa['TransitGatewayAttachmentId'] for tgwa in tgwas]
    logger.info("Transit Gateway Attachments in VPC {}:".format(vpc_id))
    
    counter = 0
    for tgwa in tgwas:
        ctgwa = f'\033[31m{tgwa}\033[00m'
        logger.info(ctgwa)
        counter += 1
    logger.info(f'\033[31mTotal: {counter}\033[00m')
    logger.info("--------------------------------------------")
    return


def describe_vpc_epts():
    epts = vpc_client.describe_vpc_endpoints(Filters=[{"Name": "vpc-id",
                                                       "Values": [vpc_id]}])['VpcEndpoints']
    epts = [ept['VpcEndpointId'] for ept in epts]
    logger.info("VPC Endpoints in VPC {}:".format(vpc_id))
    
    counter = 0
    for ept in epts:
        cept = f'\033[31m{ept}\033[00m'
        logger.info(cept)
        counter += 1
    logger.info(f'\033[31mTotal: {counter}\033[00m')
    logger.info("--------------------------------------------")
    return


def describe_vpngws(): 
    vpngws = vpc_client.describe_vpn_gateways(
        Filters=[{"Name": "attachment.vpc-id",
                  "Values": [vpc_id]}])['VpnGateways']

    vpngws = [vpngw['VpnGatewayId'] for vpngw in vpngws]

    logger.info("VPN GWs in VPC {}:".format(vpc_id))
    
    counter = 0
    for vpngw in vpngws:
        cvpngw = f'\033[31m{vpngw}\033[00m'
        logger.info(cvpngw)
        counter += 1
    logger.info(f'\033[31mTotal: {counter}\033[00m')
    logger.info("--------------------------------------------")
    return


##### END


def describe_asgs():
    logger.info("ASGs in VPC {}:".format(vpc_id))
    asgs = asg_client.describe_auto_scaling_groups()['AutoScalingGroups']
    counter = 0
    for asg in asgs:
        asg_name = asg['AutoScalingGroupName']
        if asg_in_vpc(asg):
            logger.info(asg_name)
            counter += 1
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return 


def asg_in_vpc(asg):
    subnets_list = asg['VPCZoneIdentifier'].split(',')
    for subnet in subnets_list:
        try:
            sub_description = vpc_client.describe_subnets(SubnetIds=[subnet])['Subnets']
            if sub_description[0]['VpcId'] == vpc_id:
                logger.info("{} resides in {}".format(asg['AutoScalingGroupName'], vpc_id))
                return True
        except ClientError:
            pass

    return False


def describe_ekss():
    ekss = eks_client.list_clusters()['clusters']

    logger.info("EKSs in VPC {}:".format(vpc_id))
    counter = 0
    for eks in ekss:
        eks_desc = eks_client.describe_cluster(name=eks)['cluster']
        if eks_desc['resourcesVpcConfig']['vpcId'] == vpc_id:
            logger.info(eks_desc['name'])
        counter += 1
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return


def describe_ec2s():
    waiter = vpc_client.get_waiter('instance_terminated')
    reservations = vpc_client.describe_instances(Filters=[{"Name": "vpc-id",
                                                           "Values": [vpc_id]}])['Reservations']

    ec2s = [ec2['InstanceId'] for reservation in reservations for ec2 in reservation['Instances']]

    logger.info("EC2s in VPC {}:".format(vpc_id))
    counter = 0
    for ec2 in ec2s:
        logger.info(ec2)
        counter += 1
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return


def describe_lambdas():
    lmbds = lambda_client.list_functions()['Functions']

    lambdas_list = [lmbd['FunctionName'] for lmbd in lmbds
                    if 'VpcConfig' in lmbd and lmbd['VpcConfig']['VpcId'] == vpc_id]

    logger.info("Lambdas in VPC {}:".format(vpc_id))
    counter = 0
    for lmbda in lambdas_list:
        logger.info(lmbda)
        counter += 1
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return


def describe_rdss():
    rdss = rds_client.describe_db_instances()['DBInstances']

    rdsss_list = [rds['DBInstanceIdentifier'] for rds in rdss if rds['DBSubnetGroup']['VpcId'] == vpc_id]

    logger.info("RDSs in VPC {}:".format(vpc_id))
    counter = 0
    for rds in rdsss_list:
        logger.info(rds)
        counter += 1
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return


def describe_elbs():
    elbs = elb_client.describe_load_balancers()['LoadBalancerDescriptions']

    elbs = [elb['LoadBalancerName'] for elb in elbs if elb['VPCId'] == vpc_id]

    logger.info("ELBs V1 in VPC {}:".format(vpc_id))
    counter = 0
    for elb in elbs:
        logger.info(elb)
        counter += 1
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return


def describe_elbsV2():
    elbs = elbV2_client.describe_load_balancers()['LoadBalancers']

    elbs_list = [elb['LoadBalancerArn'] for elb in elbs if elb['VpcId'] == vpc_id]

    logger.info("ELBs V2 in VPC {}:".format(vpc_id))
    counter = 0
    for elb in elbs_list:
        logger.info(elb)
        counter += 1
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return



def describe_enis():
    enis = vpc_client.describe_network_interfaces(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])['NetworkInterfaces']

    # Get a list of enis
    enis = [eni['NetworkInterfaceId'] for eni in enis]

    logger.info("ENIs in VPC {}:".format(vpc_id))
    counter = 0
    for eni in enis:
        ceni = f'\033[96m{eni}\033[00m'
        logger.info(eni)
        counter += 1
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return


def describe_subnets():
    subnets = vpc_client.describe_subnets(Filters=[{"Name": "vpc-id",
                                                    "Values": [vpc_id]}])['Subnets']

    subnets = [subnet['SubnetId'] for subnet in subnets]

    logger.info("Subnets in VPC {}:".format(vpc_id))
    counter = 0
    for subnet in subnets:
        logger.info(subnet)
        counter += 1
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return


def describe_acls():
    acls = vpc_client.describe_network_acls(Filters=[{"Name": "vpc-id",
                                                      "Values": [vpc_id]}])['NetworkAcls']

    # Get a list of subnets
    acls = [acl['NetworkAclId'] for acl in acls]
    logger.info("ACLs in VPC {}:".format(vpc_id))
    
    counter = 0
    for acl in acls:
        logger.info(acl)
        counter += 1
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return


def describe_sgs():
    sgs = vpc_client.describe_security_groups(Filters=[{"Name": "vpc-id",
                                                        "Values": [vpc_id]}])['SecurityGroups']
    # sgs = [sg['GroupId'] for sg in sgs]
    logger.info("SGs in VPC {}:".format(vpc_id))
    
    counter = 0
    for sg in sgs:
        logger.info(sg['GroupId'])
        counter += 1
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return


def describe_rtbs():
    rtbs = vpc_client.describe_route_tables(Filters=[{"Name": "vpc-id",
                                                      "Values": [vpc_id]}])['RouteTables']
    # Get a list of Routing tables
    rtbs = [rtb['RouteTableId'] for rtb in rtbs]
    logger.info("Routing tables in VPC {}:".format(vpc_id))
    counter = 0
    for rtb in rtbs:
        logger.info(rtb)
        counter += 1
    logger.info(f'Total: {counter}')
    logger.info("--------------------------------------------")
    return 





if __name__ == '__main__':

    if vpc_in_region():
        ## Gateways, Peering & Endpoints 
        describe_igws()
        describe_nats()
        describe_vpc_peering_connections_accepter()
        describe_vpc_peering_connections_requester()
        describe_tgwas()
        describe_vpc_epts()
        describe_vpngws()
        
        ## AWS resources 
        describe_subnets()
        describe_rtbs()
        describe_sgs()
        describe_acls()
        describe_enis()
        describe_ec2s()
        describe_asgs() 
        describe_elbs()
        describe_elbsV2() 
        describe_rdss()
        describe_ekss()
        describe_lambdas()
           
       
        
        
        
    else:
        logger.info("The given VPC was not found in {}".format(args.region))
