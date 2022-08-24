resource "test_get" "test_get" {
  name = "test-get"
}

resource "test_get_starts_with.ignored_suffix" "test_get_starts_with" {
  name = "test-get-starts-with.ignored-suffix"
}

resource "test_squash_terraform" "test_squash_terraform" {
  name = "test-squash-terraform"
}