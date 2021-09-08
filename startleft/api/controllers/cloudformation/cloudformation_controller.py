from fastapi import APIRouter, File, UploadFile, Form, Header

from examples import paths
from startleft import cli
from startleft.api.api_config import ApiConfig
from startleft.api.controllers.cloudformation.file_type import FileType
from startleft.api.error_response import ErrorResponse

router = APIRouter(
    prefix="/api/beta/startleft/cloudformation",
    tags=["cloudformation"],
    responses={
        201: {"description": "Provided CloudFormation Template has been processes successfully and a new IriusRisk"
                             "project has been created with the provided metadata."},
        400: {"description": "Bad request",
              "model": ErrorResponse},
        401: {"description": "Authentication information is missing or invalid or not granted to perform this action.",
              "model": ErrorResponse},
        403: {"description": "Forbidden operation",
              "model": ErrorResponse},
        404: {"description": "Not found",
              "model": ErrorResponse}},
)


@router.post("", status_code=201)
def cloudformation(cft_file: UploadFile = File(..., description="File that contains the CloudFormation Template"),
                   mapping_file: UploadFile = File(None, description="File that contains the mapping between AWS components and IriusRisk components."),
                   id: str = Form(..., description="ID of the new project"),
                   name: str = Form(..., description="Name of the new project"),
                   type: FileType = Form(..., description="Format of the CloudFormation Template"),
                   api_token: str = Header(...)
                   ):
    # Add custom mapping provided by customer
    cf_mapping_files = paths.default_cf_mapping_files
    if mapping_file:
        cf_mapping_files.append(mapping_file.file)

    # Run client
    cli.inner_run(type=type, map=cf_mapping_files, otm='threatmodel.otm', name=name, id=id,
                  ir_map=paths.default_ir_map, recreate=1, server=ApiConfig.get_iriusrisk_server(), api_token=api_token,
                  filename=[cft_file.file])
