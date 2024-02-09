#!/usr/bin/python3
import boto3
import json
from pydantic import BaseModel 
from datetime import datetime
from typing import List
import subprocess

AWS_REGION         = 'us-west-2'
ACCOUNT_ID         = ['069442728920','Network']
TRANSIT_GATEWAY_ID = 'tgw-0d36c9c74d9eac7e5'
STATE              = 'active'
IPAM_SCOPE         = 'ipam-scope-03405e286ee1a361f'

class Route(BaseModel):
    tg_route_table_id: str = ''
    tga_id: str = ''
    destination_cidr: str = ''
    tga_resource_id: str = ''
    ipam_vpc_name: str = ''
    ipam_account_id: str = ''
    tga_resource_type: str = ''    
    type: str = ''

client = boto3.client('ec2', region_name=AWS_REGION)
response = client.get_ipam_resource_cidrs(
    DryRun=False,
    IpamScopeId=IPAM_SCOPE,
    ResourceType='vpc',
    )
    
ipam_json_dump = json.dumps(response, indent=4, sort_keys=True, default=str)
### DEBUG ***************************************************************
# print(ipam_json_dump)
# with open('vpc_json_dump.json', 'w') as f:
#     json.dump(ipam_json_dump, f)


def ipam_query(ipam_json_dump, resource_id):
    vpc_json = json.loads(ipam_json_dump)['IpamResourceCidrs']
    


    resource_owner = '' 
    resource_name = ''
    for vpc in vpc_json:
        try:
            resource_owner = vpc['ResourceOwnerId']
        except KeyError:
            resource_name = 'n/a'
        try: 
            resource_name  = vpc['ResourceName']
        except KeyError:
            resource_name = 'n/a'
        
        if vpc['ResourceId'] == resource_id: 
            return resource_owner, resource_name
        
    return 'not found', 'not found'

### Test ***************************************************************
# ipam_query(ipam_json_dump, 'vpc-fb6aec9e')

def tg_route_table_ids(transit_gateway_id):
    client = boto3.client('ec2', region_name=AWS_REGION)
    response = client.describe_transit_gateway_route_tables(
        Filters=[
            {
                'Name': 'transit-gateway-id',
                'Values': [
                    transit_gateway_id,
                ]
            },
        ]   
    )

    json_dump = json.dumps(response, indent=4, sort_keys=True, default=str)
    ### DEBUG *************************************************************** 
    # print(json_dump)

    tgrt_ids_json = json.loads(json_dump)['TransitGatewayRouteTables']
    ### DEBUG ***************************************************************     
    # print(tgrt_ids_json)
    
    tg_route_table_ids = [] 
    for t in tgrt_ids_json:
        tg_route_table_id = t['TransitGatewayRouteTableId']
        tg_route_table_ids.append(tg_route_table_id)
    
    ### DEBUG *************************************************************** 
    # print(tg_route_table_ids)
    return tg_route_table_ids

def routes(tg_route_table_id):
    client = boto3.client('ec2', region_name=AWS_REGION)
    
    response = client.search_transit_gateway_routes(
        TransitGatewayRouteTableId = tg_route_table_id,
        Filters=[
            {
                'Name': 'state',
                'Values': [
                    STATE,
                ]
            },
        ],
    )

    json_dump = json.dumps(response, indent=4, sort_keys=True, default=str)
    
    ### DEBUG *************************************************************** 
    # print(json_dump)
      
    routes_json = json.loads(json_dump)['Routes']

    routes: List[Route] = []
    for f in routes_json:
        route = Route()
        route.tg_route_table_id = tg_route_table_id
        route.destination_cidr = f['DestinationCidrBlock']
        route.tga_resource_id = f['TransitGatewayAttachments'][0]['ResourceId']
        route.tga_resource_type = f['TransitGatewayAttachments'][0]['ResourceType']
        route.tga_id = f['TransitGatewayAttachments'][0]['TransitGatewayAttachmentId']
        route.type = f['Type']
        if (route.tga_resource_type == 'vpc'):
            route.ipam_account_id = ipam_query(ipam_json_dump, route.tga_resource_id)[0]
            route.ipam_vpc_name   = ipam_query(ipam_json_dump, route.tga_resource_id)[1]
        else:
            route.ipam_account_id = 'n/a'
            route.ipam_vpc_name   = 'n/a'

        routes.append(route)
    
    return routes


if __name__ == '__main__':
    print('Running...')
    tgrts = tg_route_table_ids(TRANSIT_GATEWAY_ID)

    file_name = f'TG_routes_{TRANSIT_GATEWAY_ID}_{datetime.now().strftime("%Y%m%d")}.csv'
    file = open(file_name,'w')

    csv = ''
    first = routes(tgrts[0])
    if (len(first) > 0):
        for key, value in first[0]:
            csv += f'{key},'
        csv += '\n'

    for t in tgrts:
        rs = routes(t)
        for route in rs:
            for key, value in route:
                v = value.replace(',', ' ')
                csv += f'{v},'
            csv += '\n'
    
    file.write(csv)
    file.close()
    print('Done!')
    print(file_name)
  



