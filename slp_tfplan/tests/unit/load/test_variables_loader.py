from unittest.mock import MagicMock

from slp_tfplan.slp_tfplan.load.variables_loader import VariablesLoader

VARIABLES = {
    "v_1": {
        "value": "v_1_value"
    },
    "v_2": {
        "value": ["v_2_value"]
    },
    "v_3": ["v_3_value"],
    "v_4": {
        "a": "b"
    }
}


class TestVariablesLoader:

    def test_load_variables(self):
        # GIVEN a VariablesLoader instance
        otm = MagicMock(variables={})
        variables_loader = VariablesLoader(otm, {'variables': VARIABLES})

        # WHEN load() is called
        variables_loader.load()

        # THEN the variables are loaded into the otm
        assert otm.variables['v_1'] == 'v_1_value'
        assert otm.variables['v_2'] == ['v_2_value']
        assert 'v_3' not in otm.variables
