import logging

from fastapi import APIRouter, File, UploadFile, Form, Response

import sl_util.sl_util.json_utils as jsonUtils
from _sl_build.modules import PROCESSORS
from slp_base.slp_base.provider_resolver import ProviderResolver
from slp_base.slp_base.provider_type import EtmType
from startleft.startleft.api.controllers.otm_controller import RESPONSE_STATUS_CODE, PREFIX, controller_responses

URL = '/etm'

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=PREFIX,
    responses=controller_responses
)

provider_resolver = ProviderResolver(PROCESSORS)

@router.post(URL, status_code=RESPONSE_STATUS_CODE,
             description="Generates an OTM threat model from a Threat Model file",
             tags=['Threat Model'])
def etm(source_file: UploadFile = File(..., description="File that contains the original Threat model"),
        source_type: EtmType = Form(..., description="Type of Diagram File: MTMT"),
        id: str = Form(..., description="ID of the new project"),
        name: str = Form(..., description="Name of the new project"),
        default_mapping_file: UploadFile = File(..., description="File that contains the default mapping file"),
        custom_mapping_file: UploadFile = File(None, description="File that contains the user custom mapping file")):
    logger.info(
        f"POST request received for creating new project with id {id} and name {name} from Diagram {source_type} file")

    logger.info("Parsing Threat Model file to OTM")

    with source_file.file as f:
        etm_data = f.read()

    mapping_data_list = []

    with default_mapping_file.file as f:
        mapping_data_list.append(f.read())

    if custom_mapping_file:
        with custom_mapping_file.file as f:
            mapping_data_list.append(f.read())

    processor = provider_resolver.get_processor(source_type, id, name, etm_data, mapping_data_list)
    otm = processor.process()

    return Response(status_code=201, media_type="application/json", content=jsonUtils.get_otm_as_json(otm))
