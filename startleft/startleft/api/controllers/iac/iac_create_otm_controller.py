import logging
from typing import List

from fastapi import APIRouter, File, UploadFile, Form, Response

from _sl_build.modules import PROCESSORS
from sl_util.sl_util.json_utils import get_otm_as_json
from slp_base import IacFileNotValidError,  MappingFileNotValidError
from slp_base.slp_base.provider_resolver import ProviderResolver
from slp_base.slp_base.provider_type import IacType
from startleft.startleft.api.check_mime_type import check_mime_type
from startleft.startleft.api.controllers.otm_controller import RESPONSE_STATUS_CODE, PREFIX, controller_responses

URL = '/iac'

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=PREFIX,
    tags=["IaC"],
    responses=controller_responses
)

provider_resolver = ProviderResolver(PROCESSORS)


@router.post(URL, status_code=RESPONSE_STATUS_CODE)
@check_mime_type('iac_file', 'iac_type', IacFileNotValidError)
def iac(iac_file: List[UploadFile]
        = File(...),
        iac_type: IacType = Form(...),
        id: str = Form(...),
        name: str = Form(...),
        mapping_file: UploadFile = File(None),
        default_mapping_file: UploadFile = File(None),
        custom_mapping_file: UploadFile = File(None)):
    logger.info(f"POST request received for creating new project with id {id} and name {name} from IaC {iac_type} file")

    logger.info("Parsing Threat Model file to OTM")
    iac_data = []
    for iac_file_element in iac_file:
        with iac_file_element.file as f:
            iac_data.append(f.read())

    mapping_data_list = _determine_source_file(mapping_file, default_mapping_file)

    if custom_mapping_file:
        with custom_mapping_file.file as f:
            mapping_data_list.append(f.read())

    processor = provider_resolver.get_processor(iac_type, id, name, iac_data, mapping_data_list)
    otm = processor.process()

    return Response(status_code=201, media_type="application/json", content=get_otm_as_json(otm))


def _determine_source_file(mapping_file: File, default_mapping_file: File):
    mapping_data_list = []
    if mapping_file and default_mapping_file:
        msg = "default_mapping_file and mapping_file cannot be present at the same time"
        raise MappingFileNotValidError("Error processing mapping file", msg, msg)

    if not mapping_file and not default_mapping_file:
        msg = "Mapping file must no be void"
        raise MappingFileNotValidError("Error processing mapping file", msg, msg)

    if mapping_file:
        with mapping_file.file as f:
            mapping_data_list.append(f.read())

    if default_mapping_file:
        with default_mapping_file.file as f:
            mapping_data_list.append(f.read())
    return mapping_data_list
