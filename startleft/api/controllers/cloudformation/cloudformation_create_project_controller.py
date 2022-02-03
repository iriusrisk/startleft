from fastapi import APIRouter, File, UploadFile, Form, Header

from startleft import cli
from startleft.api.api_config import ApiConfig
from startleft.api.controllers.cloudformation.file_type import FileType
from startleft.api.error_response import ErrorResponse
from startleft.messages import messages

PREFIX = '/api/v1/startleft/cloudformation'
URL = ''
RESPONSE_BODY = {}
RESPONSE_STATUS_CODE = 201

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

    mapping_files = [mapping_file.file] if mapping_file else []

    # Run client
    cli.inner_run(type=type, map=mapping_files, otm='threatmodel.otm', name=name, id=id,
                  recreate=1, irius_server=ApiConfig.get_iriusrisk_server(),
                  api_token=api_token, filename=[cft_file.file])

    return RESPONSE_BODY
