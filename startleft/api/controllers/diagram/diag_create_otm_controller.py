import logging

from fastapi import APIRouter, File, UploadFile, Form, Response

import startleft.utils.json_utils as json_utils
from slp_visio.slp_visio.diagram_type import DiagramType
from slp_visio.slp_visio.visio_processor import VisioProcessor
from startleft.api.controllers.otm_controller import RESPONSE_STATUS_CODE, PREFIX, controller_responses
from startleft.api.errors import LoadingSourceFileError

URL = '/diagram'

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=PREFIX,
    responses=controller_responses
)


def get_processor(source_type, id_, name, etm_data, mapping_data_list):
    if source_type == DiagramType.VISIO:
        return VisioProcessor(id_, name, etm_data, mapping_data_list)
    else:
        raise LoadingSourceFileError(f'{source_type} is not a supported type for source data')


@router.post(URL, status_code=RESPONSE_STATUS_CODE, description="Generates an OTM threat model from an Diagram file",
             tags=['Diagram'])
def diagram(diag_file: UploadFile = File(..., description="File that contains the diagram definition"),
            diag_type: DiagramType = Form(..., description="Type of Diagram File: VISIO"),
            id: str = Form(..., description="ID of the new project"),
            name: str = Form(..., description="Name of the new project"),
            default_mapping_file: UploadFile = File(..., description="File that contains the default mapping file"),
            custom_mapping_file: UploadFile = File(None, description="File that contains the user custom mapping file")):
    logger.info(
        f"POST request received for creating new project with id {id} and name {name} from Diagram {diag_type} file")

    logger.info("Parsing Diagram file to OTM")

    mapping_data_list = []

    with default_mapping_file.file as f:
        mapping_data_list.append(f.read())

    if custom_mapping_file:
        with custom_mapping_file.file as f:
            mapping_data_list.append(f.read())

    processor = get_processor(diag_type, id, name, diag_file, mapping_data_list)
    otm = processor.process()

    return Response(status_code=201, media_type="application/json", content=json_utils.get_otm_as_json(otm))
