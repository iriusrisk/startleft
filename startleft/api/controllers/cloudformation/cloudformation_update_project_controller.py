from fastapi import APIRouter, File, UploadFile, Form, Header, Response

from startleft import cli
from startleft.api.api_config import ApiConfig
from startleft.api.controllers.cloudformation.file_type import FileType
from startleft.api.error_response import ErrorResponse
from startleft.messages import messages

PREFIX = '/api/v1/startleft/cloudformation'
URL = ''
RESPONSE_STATUS_CODE = 204
RESPONSE_BODY = Response(status_code=RESPONSE_STATUS_CODE)

router = APIRouter(
    prefix=PREFIX,
    tags=["cloudformation"],
    responses={
        204: {"description": messages.PROJECT_SUCCESSFULLY_UPDATED},
        400: {"description": messages.BAD_REQUEST,
              "model": ErrorResponse},
        401: {"description": messages.UNAUTHORIZED_EXCEPTION,
              "model": ErrorResponse},
        403: {"description": messages.FORBIDDEN_OPERATION,
              "model": ErrorResponse},
        404: {"description": messages.PROJECT_NOT_FOUND,
              "model": ErrorResponse}}
)


@router.put('/projects/{project_id}', status_code=RESPONSE_STATUS_CODE)
def cloudformation(project_id: str,
                   cft_file: UploadFile = File(..., description="File that contains the CloudFormation Template"),
                   type: FileType = Form(..., description="Format of the CloudFormation Template"),
                   name: str = Form(..., description="Name of the project to update"),
                   api_token: str = Header(None, description="IriusRisk API token"),
                   mapping_file: UploadFile = File(None, description="File that contains the mapping between AWS "
                                                                     "components and IriusRisk components. Providing "
                                                                     "this file will completely override default values"
                                                   )
                   ):

    mapping_files = [mapping_file.file] if mapping_file else []

    # Run client
    cli.inner_run(type=type, map=mapping_files, otm='threatmodel.otm', name=name, id=project_id,
                  recreate=0, irius_server=ApiConfig.get_iriusrisk_server(),
                  api_token=api_token, filename=[cft_file.file])

    return RESPONSE_BODY
