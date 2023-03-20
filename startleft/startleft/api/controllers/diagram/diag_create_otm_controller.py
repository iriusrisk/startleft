import logging

from fastapi import APIRouter, File, UploadFile, Form, Response

from _sl_build.modules import PROCESSORS
from sl_util.sl_util.json_utils import get_otm_as_json
from slp_base import DiagramType
from slp_base.slp_base.provider_resolver import ProviderResolver
from startleft.startleft.api.check_mime_type import check_mime_type
from startleft.startleft.api.controllers.otm_controller import RESPONSE_STATUS_CODE, PREFIX, controller_responses

URL = '/diagram'

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=PREFIX,
    responses=controller_responses
)

provider_resolver = ProviderResolver(PROCESSORS)


@router.post(URL, status_code=RESPONSE_STATUS_CODE, description="Generates an OTM threat model from an Diagram file",
             tags=['Diagram'])
@check_mime_type('diag_file', 'diag_type')
def diagram(diag_file: UploadFile = File(..., description="File that contains the diagram definition"),
            diag_type: DiagramType = Form(..., description="Type of Diagram File: VISIO, LUCID"),
            id: str = Form(..., description="ID of the new project"),
            name: str = Form(..., description="Name of the new project"),
            default_mapping_file: UploadFile = File(..., description="File that contains the default mapping file"),
            custom_mapping_file: UploadFile = File(None,
                                                   description="File that contains the user custom mapping file")):
    logger.info(
        f"POST request received for creating new project with id {id} and name {name} from Diagram {diag_type} file")

    logger.info("Parsing Diagram file to OTM")

    mapping_data_list = []

    with default_mapping_file.file as f:
        mapping_data_list.append(f.read())

    if custom_mapping_file:
        with custom_mapping_file.file as f:
            mapping_data_list.append(f.read())

    processor = provider_resolver.get_processor(diag_type, id, name, diag_file, mapping_data_list, diag_type=diag_type)
    otm = processor.process()

    return Response(status_code=201, media_type="application/json", content=get_otm_as_json(otm))
