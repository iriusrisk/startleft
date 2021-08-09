load helpers/bats-support/load
load helpers/bats-assert/load
load helpers/setup
load helpers/teardown

teardown() {
  if [ "$BATS_TEST_NUMBER" -eq ${#BATS_TEST_NAMES[@]} ]; then
    teardown_common
  fi
}

@test "validate map valid" {
    cat <<'EOF' > bats_test_map.yaml
trustzones: []
components: []
dataflows: []
EOF
    run startleft validate --map bats_test_map.yaml
    assert_success
    assert_output --partial 'Mapper file is valid'
}

@test "validate map invalid" {
    cat <<'EOF' > bats_test_map.yaml
something: []
else: []
alsonotvalid: []
EOF
    run startleft validate --map bats_test_map.yaml
    assert_failure
    assert_output --partial 'Mapping files are not valid'
}

@test "validate otm valid" {
    cat <<'EOF' > bats_test_otm.otm
project:
  name: a
  id: a
trustzones: []
components: []
dataflows: []
EOF
    run startleft validate --otm bats_test_otm.otm
    assert_success
    assert_output --partial 'OTM file is valid'
}

@test "validate otm invalid" {
    cat <<'EOF' > bats_test_otm.otm
something:
  bleh: moo
else: []
alsonotvalid: []
EOF
    run startleft validate --otm bats_test_otm.otm
    assert_failure
    assert_output --partial 'OTM file is not valid'
}