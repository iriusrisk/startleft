# Oringally from from https://github.com/jasonkarns/bats-assert

flunk() {
  { if [ "$#" -eq 0 ]; then cat -
    else echo "$@"
    fi
  } | sed "s:${BATS_TMPDIR}:\${BATS_TMPDIR}:g" >&2
  return 1
}

assert_file_equals() {
    cmp --silent "$1" "$2" || {
        echo "expecting content of file $1"
        echo "to equal $2"
        cat "$1"
    } | flunk
}

assert_file_contains_count() {
  count=$($(type -p ggrep grep | head -1) -c "$2" $1)
  expr="${count}${3}"
  assert_equal $((expr)) 1 || {
    echo "looking for: $2"
    echo "in: $1"
    echo "expected: $3"
    echo "found: $count"
    echo "file content:"
    cat $1
    echo
  } | flunk
}

assert_file_contains() {
  assert_file_contains_count $1 "$2" ">0" || {
    echo "looking for :$2"
    echo "in: $1"
    echo "expected: >0"
    echo "found: 0"
    echo "file content:"
    cat $1
    echo
  } | flunk
}
