resource "unknown_resource" "name" {
  name = "name"

  ip_set_descriptor {
    type  = "IPV4"
    value = "192.0.7.0/24"
  }
}