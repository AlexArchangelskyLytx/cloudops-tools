#!/usr/bin/python3
import boto3
import json
from pydantic import BaseModel 
from datetime import datetime
from typing import List

AWS_REGION         = 'us-west-2'
ACCOUNT_ID         = ['069442728920','Network']
TRANSIT_GATEWAY_ID = 'tgw-0d36c9c74d9eac7e5'
STATE              = 'active'

class Route(BaseModel):
    tg_route_table_id: str = ''
    destination_cidr: str = ''
    tga_resource_id: str = ''
    tga_resource_type: str = ''
    tga_id: str = ''
    type: str = ''

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
        
        routes.append(route)
    
    return routes


if __name__ == '__main__':
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
  

#####
# response = client.describe_transit_gateways(
    #     # TransitGatewayIds=[
    #     #     '',
    #     # ],
    #     # Filters=[
    #     #     {
    #     #         'Name': 'string',
    #     #         'Values': [
    #     #             'string',
    #     #         ]
    #     #     },
    #     # ],
    #     # MaxResults=123,
    #     # NextToken='string',
    #     # DryRun=True|False
    #     )
    

    # response = client.describe_transit_gateway_attachments(
    #     # TransitGatewayAttachmentIds=[
    #     # 'string',
    #     # ],
    #     Filters=[
    #         {
    #             'Name': 'transit-gateway-id',
    #             'Values': [
    #                 TRANSIT_GATEWAY_ID,
    #             ]
    #         },
    #     ],
    #     MaxResults=123,
    #     # NextToken='string',
    #     # DryRun=True|False
    # )

    
