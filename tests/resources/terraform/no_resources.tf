module "aws_stack" {
  source                    = "path_to_module's_configuration_files"
  version                   = "1.0.3"
  aws_access_key_id         = var.aws_access_key_id
  aws_account_id            = var.aws_account_id
  aws_secret_access_key     = var.aws_secret_access_key
  aws_session_token         = var.aws_session_token
  region                    = var.aws_region
}

module "rds_oracle_utilities" {
  source  = "path_to_module's_configuration_files"
  version = "2.1.1"
}
