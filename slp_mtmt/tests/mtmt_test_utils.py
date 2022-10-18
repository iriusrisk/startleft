from slp_mtmt.slp_mtmt.mtmt_loader import MTMTLoader
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMappingFileLoader


def get_mtmt_from_file(filename):
    with open(filename, 'r') as f:
        xml = f.read()
    mtmt: MTMTLoader = MTMTLoader(xml)
    mtmt.load()
    return mtmt.get_mtmt()


def get_mapping_from_file(filename):
    with open(filename) as file:
        mapping_file_data = file.read()
    mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file_data])
    mtmt_mapping_file_loader.load()
    return mtmt_mapping_file_loader.get_mtmt_mapping()
