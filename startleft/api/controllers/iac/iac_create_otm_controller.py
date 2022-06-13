import logging

from fastapi import APIRouter, File, UploadFile, Form, Response

from startleft.api.controllers.otm_controller import RESPONSE_STATUS_CODE, PREFIX, controller_responses
from startleft.iac.iac_type import IacType
from startleft.otm.otm_project import OtmProject

URL = '/iac'

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=PREFIX,
    tags=["IaC"],
    responses=controller_responses
)


@router.post(URL, status_code=RESPONSE_STATUS_CODE, description="Generates an OTM threat model from an IaC file")
def iac(iac_file: UploadFile = File(..., description="File that contains the Iac definition"),
        iac_type: IacType = Form(..., description="Type of IaC File: CLOUDFORMATION, TERRAFORM"),
        id: str = Form(..., description="ID of the new project"),
        name: str = Form(..., description="Name of the new project"),
        mapping_file: UploadFile = File(..., description="File that contains the mapping between IaC "
                                                         "resources and threat model resources.")):
    logger.info(f"POST request received for creating new project with id {id} and name {name} from IaC {iac_type} file")

    logger.info("Parsing IaC file to OTM")
    with iac_file.file as f:
        iac_data = f.read()

    otm_project = OtmProject.from_iac_file_to_otm_stream(id, name, iac_type, [iac_data],
                                                         [mapping_file.file] if mapping_file else [])

    return Response(status_code=201, media_type="application/json", content=otm_project.get_otm_as_json())
