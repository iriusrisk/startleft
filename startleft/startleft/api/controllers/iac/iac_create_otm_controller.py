import logging
from typing import List

from fastapi import APIRouter, File, UploadFile, Form, Response

from _sl_build.modules import PROCESSORS
from sl_util.sl_util.json_utils import get_otm_as_json
from slp_base import IacFileNotValidError
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
        mapping_file: UploadFile = File(...)):
    logger.info(f"POST request received for creating new project with id {id} and name {name} from IaC {iac_type} file")

    logger.info("Parsing Threat Model file to OTM")
    iac_data = []
    for iac_file_element in iac_file:
        with iac_file_element.file as f:
            iac_data.append(f.read())

    mapping_data = []
    with mapping_file.file as f:
        mapping_data.append(f.read())

    processor = provider_resolver.get_processor(iac_type, id, name, iac_data, mapping_data)
    otm = processor.process()

    return Response(status_code=201, media_type="application/json", content=get_otm_as_json(otm))
