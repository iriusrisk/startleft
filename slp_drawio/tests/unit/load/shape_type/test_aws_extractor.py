import pytest
from slp_drawio.slp_drawio.load.stencil_extractors.aws_extractor import extract_aws_type


# --- Extractor function tests ---

@pytest.mark.parametrize("style, expected", [
    pytest.param("shape=mxgraph.aws4.ec2", "aws.ec2", id="simple AWS shape"),
    pytest.param("shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;", "aws.group_aws_cloud_alt", id="AWS group → grIcon"),
    pytest.param("shape=mxgraph.aws4.groupCenter;grIcon=mxgraph.aws4.group_elastic_load_balancing;", "aws.group_elastic_load_balancing", id="AWS groupCenter → grIcon"),
    pytest.param("shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.queue;", "aws.queue", id="AWS resourceIcon → resIcon"),
    pytest.param("shape=mxgraph.aws4.productIcon;prIcon=mxgraph.aws4.athena;", "aws.athena", id="AWS productIcon → prIcon"),
    pytest.param("shape=mxgraph.gcp.compute", "gcp.compute", id="Non AWS"),
])
def test_extract_aws_type_valid_cases(style, expected):
    mx_cell = {"style": style}
    result = extract_aws_type(mx_cell)
    assert result == expected


@pytest.mark.parametrize("style", [None, "", "rounded=1;"])
def test_extract_aws_type_returns_none_for_unsupported(style):
    mx_cell = {"style": style} if style is not None else {}
    result = extract_aws_type(mx_cell)
    assert result is None
