module "aws_vpc_peering_connection_default_blue" {
  source = "github.com/lytxinc/terraform-aws-network//modules/vpc-peering?ref=alex"

  # VPC peering requester
  requester_region  = "us-west-2"
  requester_profile = "datapipe-dev"          # Requester auth profile from ~/.aws/credentials
  vpc_id            = "vpc-0094a3cddd2f020cd" # datapipe-dev vpc

  # VPC peering accepter
  peer_owner_id    = "856217656037" # microservices-dev AWS account ID
  accepter_region  = "us-west-2"
  accepter_profile = "microservices-dev"     # Accepter auth profile from ~/.aws/credentials
  peer_vpc_id      = "vpc-038c1bfde1be61bfb" # microservices-dev blue default vpc

  allow_dns_resolution = true

  excluded_cidr_blocks = [
    "100.64.0.0",
    # Add more CIDR blocks to exclude as needed
  ]
}

module "aws_vpc_peering_connection_dmz_blue" {
  source = "github.com/lytxinc/terraform-aws-network//modules/vpc-peering?ref=alex"

  # VPC peering requester
  requester_region  = "us-west-2"
  requester_profile = "datapipe-dev"          # Requester auth profile from ~/.aws/credentials
  vpc_id            = "vpc-0094a3cddd2f020cd" # datapipe-dev vpc

  # VPC peering accepter
  peer_owner_id    = "856217656037" # microservices-dev AWS account ID
  accepter_region  = "us-west-2"
  accepter_profile = "microservices-dev"     # Accepter auth profile from ~/.aws/credentials
  peer_vpc_id      = "vpc-03585825bd4c979fa" # microservices-dev blue dmz vpc

  allow_dns_resolution = true

  excluded_cidr_blocks = [
    "100.64.0.0",
    # Add more CIDR blocks to exclude as needed
  ]
}

# output "peer_id" {
#   value = module.aws_vpc_peering_connection_default_blue.id
# }

# output "requester_vpc_cidr_blocks" {
#   value = module.aws_vpc_peering_connection_default_blue.requester_vpc_cidr_blocks
# }

# output "accepter_vpc_cidr_blocks" {
#   value = module.aws_vpc_peering_connection_default_blue.accepter_vpc_cidr_blocks
# }

# output "requester_route_table_ids" {
#   value = module.aws_vpc_peering_connection_default_blue.requester_route_table_ids
# }

# output "accepter_route_table_ids" {
#   value = module.aws_vpc_peering_connection_default_blue.accepter_route_table_ids
# }
