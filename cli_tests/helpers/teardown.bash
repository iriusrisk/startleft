teardown_common() {
    if [ -f "product.xml" ]; then
        rm "product.xml"
    fi

    if [ -f "diagram.xml" ]; then
        rm "diagram.xml"
    fi

    rm bats_test_*.*
}