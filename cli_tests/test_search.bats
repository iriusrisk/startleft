load helpers/bats-support/load
load helpers/bats-assert/load
load helpers/setup
load helpers/teardown

teardown() {
  if [ "$BATS_TEST_NUMBER" -eq ${#BATS_TEST_NAMES[@]} ]; then
    teardown_common
  fi
}

@test "search json" {
    cat <<'EOF' > bats_test_source.json
{
    "a": {
        "b": {
            "c": "d"
        }
    }
}
EOF
    run startleft search --type JSON --query "a.b.c" bats_test_source.json
    assert_success    
    assert_output --partial '--- Results ---
"d"'
}

@test "search hcl2" {
    cat <<'EOF' > bats_test_source.tf
a "b" {
  c = "d"
}
EOF
    run startleft search --type HCL2 --query "a[].b.c|[0]" bats_test_source.tf
    assert_success
    assert_output --partial '--- Results ---
"d"'
}

@test "search xml" {
    cat <<'EOF' > bats_test_source.xml
<a>
  <b>
    <c>
      d
    </c>
  </b>
</a>
EOF
    run startleft search --type XML --query "a.b.c" bats_test_source.xml
    assert_success
    assert_output --partial '--- Results ---
"d"'
}

