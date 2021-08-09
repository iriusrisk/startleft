load helpers/bats-support/load
load helpers/bats-assert/load
load helpers/other-asserts
load helpers/setup
load helpers/teardown

@test "parse json" {
    cat <<'EOF' > bats_test_source.json
{
    "components": [
        {
            "ref": "aref",
            "meta": {
                "name": "aname"
            }
        }
    ]
}
EOF

    cat <<'EOF' > bats_test_map.yaml
trustzones: []
components:
    - $source: {$root: "resources.components[]"}
      id: {$path: "ref"}
      name: {$path: "meta.name"}
      type: {$path: "meta.name"}
dataflows: []
EOF

    run startleft parse --map bats_test_map.yaml --otm bats_test_otm.otm --name bats_test --id bats_test bats_test_source.json
    assert_success
    
    run startleft validate --otm bats_test_otm.otm
    assert_success
}