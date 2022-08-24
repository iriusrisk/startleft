
module "unknown_module_name" {
  source      = "some_git_repository/project_name/unknown_module_name/aws"
  version     = "0.1.0"

}

resource "none_resources" "none_resources" {}