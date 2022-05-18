import logging

from fastapi import APIRouter, File, UploadFile, Form, Response

from startleft.api.controllers.otm_controller import RESPONSE_STATUS_CODE, PREFIX, controller_responses
from startleft.project.otm_project import OtmProject
from startleft.provider import Provider

URL = '/diagram'

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=PREFIX,
    responses=controller_responses
)


@router.post(URL, status_code=RESPONSE_STATUS_CODE, description="Generates an OTM threat model from an Diagram file",
             tags=['Diagram'])
def diagram(diag_file: UploadFile = File(..., description="File that contains the Iac definition"),
            diag_type: Provider = Form(..., description="Type of Diagram File: VISIO"),
            id: str = Form(..., description="ID of the new project"),
            name: str = Form(..., description="Name of the new project"),
            mapping_file: UploadFile = File(..., description="File that contains the mapping between IaC "
                                                             "resources and threat model resources.")):
    logger.info(
        f"POST request received for creating new project with id {id} and name {name} from Diagram {diag_type} file")

    logger.info("Parsing Diagram file to OTM")
    otm_project = OtmProject.from_diag_file_to_otm_stream(id, name, diag_type, [diag_file.file],
                                                          [mapping_file.file] if mapping_file else [])

    return Response(status_code=201, media_type="application/json", content=otm_project.get_otm_as_json())
