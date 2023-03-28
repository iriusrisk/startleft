import logging

from fastapi import APIRouter, File, UploadFile, Form, Response

from _sl_build.modules import PROCESSORS
from sl_util.sl_util import json_utils
from slp_base.slp_base.provider_resolver import ProviderResolver
from slp_base.slp_base.provider_type import EtmType
from startleft.startleft.api.check_mime_type import check_mime_type
from startleft.startleft.api.controllers.otm_controller import RESPONSE_STATUS_CODE, PREFIX, controller_responses

URL = '/external-threat-model'

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=PREFIX,
    responses=controller_responses
)

provider_resolver = ProviderResolver(PROCESSORS)


@router.post(URL, status_code=RESPONSE_STATUS_CODE, tags=['Threat Model'])
@check_mime_type('source_file', 'source_type')
def etm(source_file: UploadFile = File(...),
        source_type: EtmType = Form(...),
        id: str = Form(...),
        name: str = Form(...),
        default_mapping_file: UploadFile = File(...),
        custom_mapping_file: UploadFile = File(None)):
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

    return Response(status_code=201, media_type="application/json", content=json_utils.get_otm_as_json(otm))
