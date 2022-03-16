import logging
from http import HTTPStatus

from fastapi import APIRouter, File, UploadFile, Form, Header, Response

from startleft.api.error_response import ErrorResponse
from startleft.messages import messages
from startleft.project.iriusrisk_project_repository import IriusriskProjectRepository
from startleft.project.otm_project import OtmProject
from startleft.project.otm_project_service import OtmProjectService

PREFIX = '/api/v1/products/cloudformation'
URL = ''
RESPONSE_STATUS_CODE = HTTPStatus.OK
FILE_TYPE = "CLOUDFORMATION"

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=PREFIX,
    tags=["cloudformation"],
    responses={
        200: {"description": messages.PROJECT_SUCCESSFULLY_UPDATED},
        400: {"description": messages.BAD_REQUEST,
              "model": ErrorResponse},
        401: {"description": messages.UNAUTHORIZED_EXCEPTION,
              "model": ErrorResponse},
        403: {"description": messages.FORBIDDEN_OPERATION,
              "model": ErrorResponse},
        404: {"description": messages.PROJECT_NOT_FOUND,
              "model": ErrorResponse}}
)


@router.put('/{project_id}', status_code=RESPONSE_STATUS_CODE)
def cloudformation(project_id: str,
                   cft_file: UploadFile = File(..., description="File that contains the CloudFormation Template"),
                   name: str = Form(None, description="Name of the project to update"),
                   api_token: str = Header(None, description="IriusRisk API token"),
                   mapping_file: UploadFile = File(None, description="File that contains the mapping between AWS "
                                                                     "components and IriusRisk components. Providing "
                                                                     "this file will completely override default values"
                                                   )
                   ):
    logger.info(f"PUT request received for updating a project with id {project_id} from CFT file")

    otm_service = OtmProjectService(IriusriskProjectRepository(api_token))
    if not name:
        name = otm_service.get_project_name(project_id)
        logger.debug(f"Project name '{name}'")

    logger.info("Parsing CFT file to OTM")
    otm_project = OtmProject.from_iac_file(project_id, name, FILE_TYPE, [cft_file.file],
                                           [mapping_file.file] if mapping_file else [])

    logger.info(f"Updating project {project_id}")
    otm_service = OtmProjectService(IriusriskProjectRepository(api_token))

    return otm_service.update_project(otm_project)
