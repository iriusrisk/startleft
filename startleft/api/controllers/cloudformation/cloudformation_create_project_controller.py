import logging

from fastapi import APIRouter, File, UploadFile, Form, Header

from startleft.api.controllers.cloudformation.file_type import FileType
from startleft.api.error_response import ErrorResponse
from startleft.messages import messages
from startleft.project.iriusrisk_project_repository import IriusriskProjectRepository
from startleft.project.otm_project import OtmProject
from startleft.project.otm_project_service import OtmProjectService

PREFIX = '/api/v1/startleft/cloudformation'
URL = ''
RESPONSE_BODY = {}
RESPONSE_STATUS_CODE = 201

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=PREFIX,
    tags=["cloudformation"],
    responses={
        201: {"description": messages.PROJECT_SUCCESSFULLY_CREATED},
        400: {"description": messages.BAD_REQUEST,
              "model": ErrorResponse},
        401: {"description": messages.UNAUTHORIZED_EXCEPTION,
              "model": ErrorResponse},
        403: {"description": messages.FORBIDDEN_OPERATION,
              "model": ErrorResponse}}
)


@router.post(URL, status_code=RESPONSE_STATUS_CODE)
def cloudformation(cft_file: UploadFile = File(..., description="File that contains the CloudFormation Template"),
                   type: FileType = Form(..., description="Format of the CloudFormation Template"),
                   id: str = Form(..., description="ID of the new project"),
                   name: str = Form(..., description="Name of the new project"),
                   api_token: str = Header(None, description="IriusRisk API token"),
                   mapping_file: UploadFile = File(None, description="File that contains the mapping between AWS "
                                                                     "components and IriusRisk components. Providing "
                                                                     "this file will completely override default values"
                                                   )
                   ):
    logger.info(f"POST request received for creating new project with id {id} and name {name} from CFT file")

    logger.info("Parsing CFT file to OTM")
    otm_project = OtmProject.from_iac_file(id, name, type, [cft_file.file], [mapping_file.file] if mapping_file else [])

    logger.info("Creating new project")
    otm_service = OtmProjectService(IriusriskProjectRepository(api_token))
    otm_service.create_project(otm_project)

    return RESPONSE_BODY
