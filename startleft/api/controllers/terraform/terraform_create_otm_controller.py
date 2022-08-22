import logging

from fastapi import APIRouter, File, UploadFile, Form, Response

import startleft.utils.json_utils as jsonUtils
from startleft.api.controllers.otm_controller import RESPONSE_STATUS_CODE, PREFIX, controller_responses
from startleft.api.errors import LoadingSourceFileError
from startleft.iac.iac_type import IacType
from startleft.processors.terraform.tf_processor import TerraformProcessor

URL = '/terraform'

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=PREFIX,
    tags=["Terraform"],
    responses=controller_responses
)


def get_processor(source_type, id, name, tf_data, mapping_data_list):
    if source_type == IacType.TERRAFORM:
        return TerraformProcessor(id, name, tf_data, mapping_data_list)
    else:
        raise LoadingSourceFileError(f'{source_type} is not a supported type for source data')


@router.post(URL, status_code=RESPONSE_STATUS_CODE, description="Generates an OTM threat model from an IaC file")
def terraform(iac_file: UploadFile = File(..., description="File that contains the Iac definition"),
        iac_type: IacType = Form(..., description="Type of IaC File: CLOUDFORMATION, TERRAFORM"),
        id: str = Form(..., description="ID of the new project"),
        name: str = Form(..., description="Name of the new project"),
        mapping_file: UploadFile = File(..., description="File that contains the mapping between IaC "
                                                         "resources and threat model resources.")):
    logger.info(f"POST request received for creating new project with id {id} and name {name} from IaC {iac_type} file")

    logger.info("Parsing Threat Model file to OTM")

    with iac_file.file as f:
        iac_data = f.read()

    mapping_data_list = []

    with mapping_file.file as f:
        mapping_data_list.append(f.read())

    processor = get_processor(iac_type, id, name, iac_data, mapping_data_list)
    otm = processor.process()

    return Response(status_code=201, media_type="application/json", content=jsonUtils.get_otm_as_json(otm))
