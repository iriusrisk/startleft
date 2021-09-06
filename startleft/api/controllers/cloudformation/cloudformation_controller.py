from fastapi import APIRouter, File, UploadFile, Form, Header, status

from examples import paths
from startleft import cli
from startleft.api.error_response import ErrorResponse


iriusrisk_server = 'http://localhost:8080'

router = APIRouter(
    prefix="/api/beta/startleft/cloudformation",
    tags=["cloudformation"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=ErrorResponse)
def cloudformation(cft_file: UploadFile = File(...),
                   mapping_file: UploadFile = File(None),
                   id: str = Form(...),
                   name: str = Form(...),
                   api_token: str = Header(...)
                   ):

    # Add custom mapping provided by customer
    cf_mapping_files = paths.default_cf_mapping_files
    if mapping_file:
        cf_mapping_files.append(mapping_file.file)

    # Run client
    cli.inner_run(type='YAML', map=cf_mapping_files, otm='threatmodel.otm', name=name, id=id,
                      ir_map=paths.default_ir_map, recreate=1, server=iriusrisk_server, api_token=api_token,
                      filename=[cft_file.file])

    return {}
