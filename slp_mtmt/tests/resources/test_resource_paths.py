import os

path = os.path.dirname(__file__)

# mapping
mtmt_mapping_file = f'{path}/mapping/mtmt-mapping.yaml'
default_mtmt_single_mapping_file = f'{path}/mapping/mtmt-default-mapping-single-element.yaml'
default_mtmt_multiple_mapping_file = f'{path}/mapping/mtmt-default-mapping-multiple-elements.yaml'
trustzones_no_mandatory_label_added_mtmt_mapping_file = path + \
                                                        '/mapping/mtmt-default-mapping-trustzones-no-mandatory-label-added.yaml'
no_mandatory_label_added_mtmt_mapping_file = f'{path}/mapping/mtmt-default-mapping-no-mandatory-label-added.yaml'
custom_mtmt_single_mapping_file = f'{path}/mapping/mtmt-custom-mapping-single-element.yaml'
custom_mtmt_multiple_mapping_file = f'{path}/mapping/mtmt-custom-mapping-multiple-elements.yaml'
custom_bad_formed_file = f'{path}/mapping/mtmt-custom-bad-formed-file.yaml'
default_mtmt_empty_elements = f'{path}/mapping/mtmt-default-mapping-empty-elements.yaml'
mtmt_empty_mapping_file = f'{path}/mapping/mtmt-empty-mapping.yaml'
mtmt_mapping_filled_file = f'{path}/mapping/mtmt-mapping-filled.yaml'
mapping_mtmt_mvp = f'{path}/mapping/MTMT_MVP.yaml'
mtmt_default_mapping = f'{path}/mapping/mtmt_default_mapping.yaml'
mtmt_mapping_invalid_no_dataflows = f'{path}/mapping/invalid-mapping-without-dataflows.yaml'
name_mapping_overriden = f'{path}/mapping/name_mapping_overriden.yaml'
type_mapping_overriden = f'{path}/mapping/type_mapping_overriden.yaml'


# legacy mapping
mapping_mtmt_mvp_legacy = f'{path}/mapping/MTMT_MVP_legacy.yaml'
mtmt_default_mapping_legacy = f'{path}/mapping/mtmt_default_mapping_legacy.yaml'
mapping_mtmt_mvp_no_type = f'{path}/mapping/MTMT_MVP_no_type.yaml'
mtmt_default_mapping_no_type = f'{path}/mapping/mtmt_default_mapping_no_type.yaml'
name_mapping_overriden_legacy = f'{path}/mapping/name_mapping_overriden_legacy.yaml'
type_mapping_overriden_legacy = f'{path}/mapping/type_mapping_overriden_legacy.yaml'

# mtmt
model_mtmt_source_file = f'{path}/mtmt/test_model.tm7'
model_mtmt_with_lines = f'{path}/mtmt/test_model_lines.tm7'
model_mtmt_mvp = f'{path}/mtmt/MTMT_MVP.tm7'
mtmt_sdl_all_components = f'{path}/mtmt/SDL_all_components.tm7'
mtmt_unmapped_trustzone = f'{path}/mtmt/unmapped-trustzone.tm7'
missing_position = f'{path}/mtmt/missing_coordinates.tm7'
example_position_tm7 = f'{path}/mtmt/MTMT_example_coordinates.tm7'
position_1line_tz_tm7 = f'{path}/mtmt/MTMT_example_coordinates_1_line_trustzone.tm7'
position_1orphan_tm7 = f'{path}/mtmt/MTMT_example_coordinates_1_orphan.tm7'
nested_trustzones_tm7 = f'{path}/mtmt/MTMT_nested_tz.tm7'
nested_trustzones_line_tm7 = f'{path}/mtmt/MTMT_nested_tz_line.tm7'
one_trustzone_tm7 = f'{path}/mtmt/one-trustzone.tm7'
model_with_figures_without_name_file = f'{path}/mtmt/model_with_figures_without_name.tm7'

# OTM
example_position_otm = f'{path}/mtmt/MTMT_example_coordinates.otm'
position_1line_tz_otm = f'{path}/mtmt/MTMT_example_coordinates_1_line_trustzone.otm'
position_1orphan_otm = f'{path}/mtmt/MTMT_example_coordinates_1_orphan.otm'
model_mtmt_mvp_otm = f'{path}/otm/MTMT_MVP.otm'
missing_position_otm = f'{path}/otm/missing_coordinates.otm'
nested_trustzones_otm = f'{path}/otm/nested_tz.otm'
nested_trustzones_line_otm = f'{path}/otm/nested_tz_line.otm'

