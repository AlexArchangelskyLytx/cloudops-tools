connection "aws_datapipe_dev" {
  plugin  = "aws"
  profile = "DataPipe-Dev"
  regions = ["us-west-2"]
}
connection "aws_datapipe_sbx" {
  plugin  = "aws"
  profile = "DataPipe-SBX"
  regions = ["us-west-2"]
}
connection "aws_ci_cd_ami" {
  plugin  = "aws"
  profile = "ci-cd-ami"
  regions = ["us-west-2"]
}
connection "aws_datapipe_stg" {
  plugin  = "aws"
  profile = "DataPipe-Stg"
  regions = ["us-west-2"]
}
connection "aws_datapipe_prod" {
  plugin  = "aws"
  profile = "DataPipe-Prod"
  regions = ["us-west-2"]
}
connection "aws_aml" {
  plugin  = "aws"
  profile = "AML"
  regions = ["us-west-2"]
}
connection "aws_network" {
  plugin  = "aws"
  profile = "Network"
  regions = ["us-west-2"]
}
connection "aws_noc" {
  plugin  = "aws"
  profile = "NOC"
  regions = ["us-west-2"]
}
connection "aws_aml_in" {
  plugin  = "aws"
  profile = "AML-IN"
  regions = ["us-west-2"]
}
connection "aws_audit" {
  plugin  = "aws"
  profile = "Audit"
  regions = ["us-west-2"]
}
connection "aws_dataplatform_dev" {
  plugin  = "aws"
  profile = "DataPlatform-Dev"
  regions = ["us-west-2"]
}
connection "aws_dataplatform_prod" {
  plugin  = "aws"
  profile = "DataPlatform-Prod"
  regions = ["us-west-2"]
}
connection "aws_dataplatform_stg" {
  plugin  = "aws"
  profile = "DataPlatform-Stg"
  regions = ["us-west-2"]
}
connection "aws_dataplatform_sandbox" {
  plugin  = "aws"
  profile = "DataPlatform-Sandbox"
  regions = ["us-west-2"]
}
connection "aws_eld_dev" {
  plugin  = "aws"
  profile = "ELD-Dev"
  regions = ["us-west-2"]
}
connection "aws_infra_pipeline_dev" {
  plugin  = "aws"
  profile = "Infra-Pipeline-Dev"
  regions = ["us-west-2"]
}
connection "aws_infra_pipeline_prod" {
  plugin  = "aws"
  profile = "Infra-Pipeline-Prod"
  regions = ["us-west-2"]
}
connection "aws_infra_pipeline_sbx" {
  plugin  = "aws"
  profile = "Infra-Pipeline-SBX"
  regions = ["us-west-2"]
}
connection "aws_infra_pipeline_stg" {
  plugin  = "aws"
  profile = "Infra-Pipeline-Stg"
  regions = ["us-west-2"]
}
connection "aws_kong" {
  plugin  = "aws"
  profile = "kong"
  regions = ["us-west-2"]
}
connection "aws_lab" {
  plugin  = "aws"
  profile = "Lab"
  regions = ["us-west-2"]
}
connection "aws_log_archive" {
  plugin  = "aws"
  profile = "Log-archive"
  regions = ["us-west-2"]
}
connection "aws_microservices_dev" {
  plugin  = "aws"
  profile = "MicroServices-Dev"
  regions = ["us-west-2"]
}
connection "aws_microservices_prod" {
  plugin  = "aws"
  profile = "MicroServices-Prod"
  regions = ["us-west-2"]
}
connection "aws_microservices_sbx" {
  plugin  = "aws"
  profile = "MicroServices-SBX"
  regions = ["us-west-2"]
}
connection "aws_microservices_stg" {
  plugin  = "aws"
  profile = "MicroServices-Stg"
  regions = ["us-west-2"]
}
connection "aws_payer" {
  plugin  = "aws"
  profile = "Payer"
  regions = ["us-west-2"]
}
connection "aws_pipeline_prod" {
  plugin  = "aws"
  profile = "Pipeline-Prod"
  regions = ["us-west-2"]
}
connection "aws_pipeline_sbx" {
  plugin  = "aws"
  profile = "Pipeline-SBX"
  regions = ["us-west-2"]
}
connection "aws_pipeline_stg" {
  plugin  = "aws"
  profile = "Pipeline-Stg"
  regions = ["us-west-2"]
}
connection "aws_pipeline_dev" {
  plugin  = "aws"
  profile = "Pipeline-Dev"
  regions = ["us-west-2"]
}
connection "aws_surf_dev" {
  plugin  = "aws"
  profile = "Surf-Dev"
  regions = ["us-west-2"]
}
connection "aws_surf_int" {
  plugin  = "aws"
  profile = "Surf-Int"
  regions = ["us-west-2"]
}
connection "aws_surf_perf" {
  plugin  = "aws"
  profile = "Surf-Perf"
  regions = ["us-west-2"]
}
connection "aws_surf_stg" {
  plugin  = "aws"
  profile = "Surf-Stg"
  regions = ["us-west-2"]
}
connection "aws_surf_pipeline_int" {
  plugin  = "aws"
  profile = "Surf-Pipeline-Int"
  regions = ["us-west-2"]
}
connection "aws_surf_prod_eu" {
  plugin  = "aws"
  profile = "Surf-Prod-EU"
  regions = ["us-west-2"]
}
connection "aws_surf_prod_us" {
  plugin  = "aws"
  profile = "Surf-Prod-US"
  regions = ["us-west-2"]
}



# Agg
connection "aws_all" {
  type        = "aggregator"
  plugin      = "aws"
  connections = ["aws_*"]
}
connection "aws_prod_all" {
  type        = "aggregator"
  plugin      = "aws"
  connections = ["aws_*_prod"]
}
connection "aws_stg_all" {
  type        = "aggregator"
  plugin      = "aws"
  connections = ["aws_*_stg"]
}
connection "aws_dev_all" {
  type        = "aggregator"
  plugin      = "aws"
  connections = ["aws_*_dev"]
}
connection "aws_sbx_all" {
  type        = "aggregator"
  plugin      = "aws"
  connections = ["aws_*_sbx"]
}
connection "aws_surf_all" {
  type        = "aggregator"
  plugin      = "aws"
  connections = ["aws_surf_*"]
}
