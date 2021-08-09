teardown_common() {
    if [ -f "product.xml" ]; then
        rm "product.xml"
    fi

    if [ -f "diagram.xml" ]; then
        rm "diagram.xml"
    fi

    if [ -f bats_test_*.*]; then
        rm bats_test_*.*
    fi
}