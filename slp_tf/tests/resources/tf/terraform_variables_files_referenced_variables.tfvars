## aws
aws_region    = "ap-southeast-2"
aws_profile   = "iriusrisk"

## instance
instance_name = "terraform-ha"

## iriusrisk
iriusrisk_version        = "4.5.1"
startleft_version        = "startleft"
type                     = "internal"
bastion_host_cidrs       = ["52.30.97.44/32"]
certificate_arn          = "arn:aws:iam::154977180039:server-certificate/wildcard-iriusrisk-com-until-25-oct-2022"
iam_instance_profile_arn = "arn:aws:iam::154977180039:instance-profile/myManagedInstanceRoleforSSM"

## vpc
vpc_cidr              = "10.0.0.0/16"
public_subnet_cidrs   = ["10.0.10.0/24", "10.0.11.0/24"]
private_subnet_cidrs  = ["10.0.20.0/24", "10.0.21.0/24"]
database_subnet_cidrs = ["10.0.30.0/24", "10.0.31.0/24"]
availability_zones    = ["ap-southeast-2a", "ap-southeast-2b"]

## rds
dbname               = "iriusprod"
dbuser               = "iriusprod"
dbpassword           = "alongandcomplexpassword2523"
rds_instance_type    = "db.t3.medium"
rds_engine_version   = "11.15"
rds_family           = "postgres11"
major_engine_version = "11"

## ec2
ec2_instance_type  = "t3a.medium"
key_name           = "IriusRiskAPSE2"

## auto scaling group
min_size           = 1
max_size           = 3
desired_capacity   = 1

## cloudflare
cloudflare_zone_id = "322584a91b72b6a7f152b5f548cad339"
cloudflare_token   = "find-cloudflare-api-token-in-passbolt"
