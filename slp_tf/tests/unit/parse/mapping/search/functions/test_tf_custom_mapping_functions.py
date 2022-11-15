from unittest.mock import MagicMock, call

import pytest

from slp_tf.slp_tf.parse.mapping.search.functions.tf_custom_mapping_functions import root, skip, parent, singleton, \
    catchall, hub, ip, lookup, path, format, find_first, number_of_sources, module


class TestTfCustomMappingFunctions:
    source_model_data = {
        "resource": [
            {
                "resource_type": "aws_vpc_endpoint",
                "resource_name": "VPCssm",
                "resource_properties": {
                    "vpc_id": "${aws_vpc.CustomVPC.id}",
                    "service_name": "the.service.name",
                    "vpc_endpoint_type": "Interface",
                    "security_group_ids": [
                        "${aws_security_group.VPCssmSecurityGroup.id}"
                    ],
                    "subnet_ids": [
                        "${aws_subnet.PrivateSubnet1.id}",
                        "${aws_subnet.PrivateSubnet2.id}"
                    ],
                    "private_dns_enabled": True
                }
            }
        ]
    }

    def test_root(self):
        mapping_source = {
            "$root": "resource|[?resource_type=='aws_vpc_endpoint']"
        }
        data = root(mapping_source, source_model_data=self.source_model_data)

        assert data[0] == self.source_model_data['resource'][0]

    @pytest.mark.parametrize('func_name,func',
                             [("$skip", skip), ("$parent", parent), ("$singleton", singleton),
                              ("$catchall", catchall), ("$hub", hub), ("$ip", ip)])
    def test_wrapper_method(self, func_name, func):
        mapping_source = {func_name: {
            "$root": "resource|[?Type=='aws_vpc_endpoint']"
        }}
        tf_source_model = MagicMock()
        func(mapping_source,
             tf_source_model=tf_source_model,
             source=self.source_model_data)

        tf_source_model.search.assert_has_calls([call(mapping_source[func_name], self.source_model_data)])

    def test_lookup_str(self):
        mapping_source = {"$lookup": {
            "$root": "resource|[?Type=='aws_vpc_endpoint']"
        }}
        tf_source_model = MagicMock(lookup={"key": "value"})
        tf_source_model.search.return_value = "key"
        data = lookup(mapping_source,
                      tf_source_model=tf_source_model,
                      source=self.source_model_data)

        assert data == "value"

    def test_lookup_list(self):
        mapping_source = {"$lookup": {
            "$root": "resource|[?Type=='aws_vpc_endpoint']"
        }}
        tf_source_model = MagicMock(lookup={"key1": "value1", "key2": "value2"})
        tf_source_model.search.return_value = ["key1", "key2"]
        data = lookup(mapping_source,
                      tf_source_model=tf_source_model,
                      source=self.source_model_data)

        assert data == ["value1", "value2"]

    def test_path(self):
        mapping_source = {"$path": "resource_type"}
        data = path(mapping_source, source=self.source_model_data["resource"][0])
        assert data == "aws_vpc_endpoint"

    def test_path_search_params_with_path(self):
        mapping_source = {"$path": {"$searchParams": {"searchPath": "resource_type"}}}
        data = path(mapping_source, source=self.source_model_data["resource"][0])
        assert data == "aws_vpc_endpoint"

    def test_path_search_params_with_default(self):
        mapping_source = {"$path": {"$searchParams": {"searchPath": "not_found", "defaultValue": "value_by_default"}}}
        data = path(mapping_source, source=self.source_model_data["resource"][0])
        assert data == "value_by_default"

    def test_format(self):
        mapping_source = {"$format": "{resource_type}.{resource_name}"}
        data = format(mapping_source, source=self.source_model_data["resource"][0])
        assert data == "aws_vpc_endpoint.VPCssm"

    def test_find_first(self):
        mapping_source = {"$findFirst": ["resource_type_none", "resource_type"]}
        data = find_first(mapping_source, source=self.source_model_data["resource"][0])
        assert data == "aws_vpc_endpoint"

    def test_find_first_search_params(self):
        mapping_source = {"$findFirst": {"$searchParams": {"searchPath": ["resource_type_none", "resource_type"],
                                                           "defaultValue": "default_value"}}}
        data = find_first(mapping_source, source=self.source_model_data["resource"][0])
        assert data == "aws_vpc_endpoint"

    def test_find_first_search_params_with_default(self):
        mapping_source = {"$findFirst": {"$searchParams": {"searchPath": ["resource_type_none", "resource_type_none2"],
                                                           "defaultValue": "default_value"}}}
        data = find_first(mapping_source, source=self.source_model_data["resource"][0])
        assert data == "default_value"

    def test_number_of_sources(self):
        mapping_source = {"$numberOfSources":
            {
                "oneSource": {"$path": "resource_type"},
                "multipleSource": {"$format": "{resource_name} ({resource_type})"}
            }}

        tf_source_model = MagicMock()
        number_of_sources(
            mapping_source,
            tf_source_model=tf_source_model,
            source=self.source_model_data["resource"][0])

        tf_source_model.search.assert_has_calls(
            [call(mapping_source["$numberOfSources"]["multipleSource"], self.source_model_data["resource"][0]),
             call(mapping_source["$numberOfSources"]["oneSource"], self.source_model_data["resource"][0])]
        )

    def test_module(self):
        mapping_source = {"$module": "module_name"}
        source_model_data = {
            "module": [{"test": {"source": "module_name"}}]
        }

        data = module(mapping_source, source_model_data=source_model_data)

        assert data[0]["source"] == "module_name"
