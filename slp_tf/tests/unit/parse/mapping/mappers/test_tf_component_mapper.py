from slp_tf.slp_tf.parse.mapping.mappers.tf_component_mapper import get_children


class TestTfComponentMapper:

    def test_get_children_from_source(self):
        mapping = {
            "$source": {
                "$children": True
            }
        }
        assert get_children(mapping)

    def test_get_children_from_children(self):
        mapping = {
            "children": True
        }
        assert get_children(mapping)
