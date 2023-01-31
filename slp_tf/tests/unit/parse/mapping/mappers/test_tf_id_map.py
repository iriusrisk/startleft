import pytest

from slp_tf.slp_tf.parse.mapping.mappers.tf_backward_compatibility import TfIdMapDictionary

TYPE, NAME, EXPECTED = ("aws_security_group", "VPCssmSecurityGroup", "IriusRisk")


@pytest.fixture()
def id_map():
    id_map = TfIdMapDictionary()
    id_map[f"{TYPE}.{NAME}"] = EXPECTED
    yield id_map


class TestTfIdMapDictionary:

    @pytest.mark.parametrize('key, expected', [
        pytest.param(f"{TYPE}.{NAME}", EXPECTED, id="by key"),
        pytest.param(f"{NAME}", EXPECTED, id="by backward_compatibility")
    ])
    def test_getitem(self, id_map, key, expected):
        assert id_map.get(key) == expected

    def test_getitem_by_type_name(self):
        id_map = TfIdMapDictionary()
        id_map[f"{NAME}"] = EXPECTED
        assert id_map.get(f"{TYPE}.{NAME}") == EXPECTED

    @pytest.mark.parametrize('key, expected', [
        pytest.param(f"{TYPE}.{NAME}", EXPECTED, id="by key"),
        pytest.param(f"{NAME}", EXPECTED, id="by backward_compatibility"),
        pytest.param("Not_exists", "default", id="by not existing key")])
    def test_getitem_default(self, id_map, key, expected):
        assert id_map.get(key, "default") == expected

    @pytest.mark.parametrize('key, expected', [
        pytest.param(f"{TYPE}.{NAME}", True, id="by key"),
        pytest.param(f"{NAME}", True, id="by backward_compatibility"),
        pytest.param("Not_exists", False, id="by not existing key")])
    def test_contain(self, id_map, key, expected):
        assert (key in id_map) == expected
