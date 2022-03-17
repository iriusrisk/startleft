import logging

from http import HTTPStatus

from fastapi import APIRouter, File, UploadFile, Form, Response

from startleft.api.error_response import ErrorResponse
from startleft.messages import messages
from startleft.project.otm_project import OtmProject

PREFIX = '/api/v1/startleft/cloudformation'
URL = ''
RESPONSE_STATUS_CODE = HTTPStatus.CREATED
FILE_TYPE = "CLOUDFORMATION"

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=PREFIX,
    tags=["cloudformation"],
    responses={
        201: {"description": messages.OTM_SUCCESSFULLY_CREATED},
        400: {"description": messages.BAD_REQUEST,
              "model": ErrorResponse},
        401: {"description": messages.UNAUTHORIZED_EXCEPTION,
              "model": ErrorResponse},
        403: {"description": messages.FORBIDDEN_OPERATION,
              "model": ErrorResponse},
        'default': {"description": messages.UNEXPECTED_API_ERROR,
                    "model": ErrorResponse}
    }
)


@router.post(URL, status_code=RESPONSE_STATUS_CODE)
def cloudformation(cft_file: UploadFile = File(..., description="File that contains the CloudFormation Template"),
                   id: str = Form(..., description="ID of the new project"),
                   name: str = Form(..., description="Name of the new project"),
                   mapping_file: UploadFile = File(None, description="File that contains the mapping between AWS "
                                                                     "components and IriusRisk components. Providing "
                                                                     "this file will completely override default values"
                                                   )
                   ):
    logger.info(f"POST request received for creating new project with id {id} and name {name} from CFT file")

    logger.info("Parsing CFT file to OTM")
    otm_project = OtmProject.from_iac_file(id, name, FILE_TYPE, [cft_file.file], [mapping_file.file] if mapping_file else [])

    logger.info("Creating new project")

    return Response(status_code=201, media_type="application/json", content=open(otm_project.otm_filename, 'rb').read())
