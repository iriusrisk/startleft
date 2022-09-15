import json
import logging
import re
import sys

import click

from _sl_build.modules import PROCESSORS
from otm.otm.otm import OTM
from sl_util.sl_util.file_utils import get_data
from slp_base import CommonError
from slp_base import DiagramType, OtmGenerationError
from slp_base import IacType
from slp_base.slp_base.otm_file_loader import OtmFileLoader
from slp_base.slp_base.otm_validator import OtmValidator
from slp_base.slp_base.provider_resolver import ProviderResolver
from slp_cft.slp_cft.cft_searcher import CloudformationSearcher
from slp_tf.slp_tf.tf_searcher import TerraformSearcher
from startleft.startleft.cli.clioptions.exclusion_option import Exclusion
from startleft.startleft.messages import *
from startleft.startleft.version import version
from startleft.startleft.api import fastapi_server
from startleft.startleft.log import get_log_level, configure_logging

logger = logging.getLogger(__name__)
provider_resolver = ProviderResolver(PROCESSORS)


def get_otm_as_file(otm: OTM, out_file: str):
    logger.info(f"Writing OTM file to '{out_file}'")
    try:
        with open(out_file, "w") as f:
            json.dump(otm.json(), f, indent=2)
    except Exception as e:
        logger.error(f"Unable to create the threat model: {e}")
        raise OtmGenerationError("Unable to create the OTM", e.__class__.__name__, str(e.__cause__))


def validate_server(ctx, param, value):
    regex = "((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}(\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*))?(:[0-9]+)?"
    p = re.compile(regex)

    if value is None or not re.search(p, value):
        raise click.BadParameter("IriusRisk host must follow the convention 'proto://server[:port]'")

    return value


def get_iac_searcher(iac_type, iac_data: [bytes]):
    if iac_type.upper() == 'CLOUDFORMATION':
        return CloudformationSearcher(iac_data)
    elif iac_type.upper() == 'TERRAFORM':
        return TerraformSearcher(iac_data)


class CatchAllExceptions(click.Group):
    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except CommonError as e:
            logger.exception(e.message)
            sys.exit(e.error_code.system_exit_status)
        except Exception as exc:
            logger.exception(exc)


@click.group(cls=CatchAllExceptions)
@click.option('--log-level', '-l',
              type=click.Choice(['CRIT', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'NONE'], case_sensitive=False),
              callback=get_log_level, default='info', help='Set the log level.')
@click.option('--verbose/--no-verbose', '-v/-nv', default=False, help='Makes logging more verbose.')
@click.version_option(version)
def cli(log_level, verbose):
    """
    Parse IaC and other files to the Open Threat Model format
    """
    configure_logging(verbose, log_level)


def parse_iac(iac_type, mapping_file, output_file, project_name, project_id, iac_files):
    """
    Parses IaC source files into Open Threat Model
    """
    logger.info("Parsing IaC source files into OTM")
    iac_data = []
    for iac_file in iac_files:
        iac_data.append(get_data(iac_file))

    mapping_data = [get_data(mapping_file)]

    processor = provider_resolver.get_processor(IacType(iac_type.upper()), project_id, project_name, iac_data,
                                                mapping_data)
    otm = processor.process()

    get_otm_as_file(otm, output_file)


def parse_diagram(diagram_type, default_mapping_file, custom_mapping_file, output_file, project_name,
                  project_id, diag_file):
    """
    Parses diagram source files into Open Threat Model
    """
    logger.info("Parsing diagram source files into OTM")
    type_ = DiagramType(diagram_type.upper())
    file = open(diag_file[0], "r")

    mapping_data_list = [get_data(default_mapping_file)]

    if custom_mapping_file:
        mapping_data_list.append(get_data(custom_mapping_file))

    processor = provider_resolver.get_processor(type_, project_id, project_name, file, mapping_data_list)
    otm = processor.process()
    get_otm_as_file(otm, output_file)


@cli.command(name='parse')
@click.option(IAC_TYPE_NAME, IAC_TYPE_SHORTNAME,
              type=click.Choice(IAC_TYPE_SUPPORTED, case_sensitive=False),
              help=IAC_TYPE_DESC,
              cls=Exclusion,
              mandatory=True,
              mutually_exclusion=['diagram_type', 'default_mapping_file', 'custom_mapping_file'])
@click.option(DIAGRAM_TYPE_NAME, DIAGRAM_TYPE_SHORTNAME,
              type=click.Choice(DIAGRAM_TYPE_SUPPORTED, case_sensitive=False),
              help=DIAGRAM_TYPE_DESC,
              cls=Exclusion,
              mandatory=True,
              mutually_exclusion=['iac_type', 'mapping_file'])
@click.option(MAPPING_FILE_NAME, MAPPING_FILE_SHORTNAME,
              help=MAPPING_FILE_DESC,
              cls=Exclusion,
              mandatory=True,
              mutually_exclusion=['default_mapping_file', 'custom_mapping_file', 'diagram_type'])
@click.option(DEFAULT_MAPPING_FILE_NAME, DEFAULT_MAPPING_FILE_SHORTNAME,
              help=DEFAULT_MAPPING_FILE_DESC,
              cls=Exclusion,
              mandatory=True,
              mutually_exclusion=['mapping_file', 'iac_type'])
@click.option(CUSTOM_MAPPING_FILE_NAME, CUSTOM_MAPPING_FILE_SHORTNAME,
              help=CUSTOM_MAPPING_FILE_DESC,
              cls=Exclusion,
              mutually_exclusion=['mapping_file', 'iac_type'])
@click.option(OUTPUT_FILE_NAME, OUTPUT_FILE_SHORTNAME, default=OUTPUT_FILE, help=OUTPUT_FILE_DESC)
@click.option(PROJECT_NAME_NAME, PROJECT_NAME_SHORTNAME, required=True, help=PROJECT_NAME_DESC)
@click.option(PROJECT_ID_NAME, PROJECT_ID_SHORTNAME, required=True, help=PROJECT_ID_DESC)
@click.argument(SOURCE_FILE_NAME, required=True, nargs=-1)
def parse_any(iac_type, diagram_type, mapping_file, default_mapping_file, custom_mapping_file,
              output_file, project_name, project_id, source_file):
    """
    Parses source files into Open Threat Model
    """
    logger.info("Parsing source files into OTM")
    if iac_type is not None:
        parse_iac(iac_type, mapping_file, output_file, project_name, project_id, source_file)
    elif diagram_type is not None:
        parse_diagram(diagram_type, default_mapping_file, custom_mapping_file, output_file, project_name,
                      project_id, source_file)
    else:
        logger.warning('Unable to determine the parser type. Not diagram either iaC.')


@cli.command()
@click.option(IAC_MAPPING_FILE_NAME, IAC_MAPPING_FILE_SHORTNAME, help=IAC_MAPPING_FILE_DESC)
@click.option(DIAGRAM_MAPPING_FILE_NAME, DIAGRAM_MAPPING_FILE_SHORTNAME, help=DIAGRAM_MAPPING_FILE_DESC)
@click.option(OTM_INPUT_FILE_NAME, OTM_INPUT_FILE_SHORTNAME, help=OTM_INPUT_FILE_DESC)
def validate(iac_mapping_file, diagram_mapping_file, otm_file):
    """
    Validates a mapping or OTM file
    """

    if iac_mapping_file:
        # TODO Cannot assume all diagram/iac mapping file will have the same validation type, so we need to request the type in the command
        logger.info("Validating IaC mapping files")
        provider_resolver.get_mapping_validator(IacType.CLOUDFORMATION, [get_data(iac_mapping_file)]).validate()

    if diagram_mapping_file:
        # TODO Cannot assume all diagram/iac mapping file will have the same validation type, so we need to request the type in the command
        logger.info("Validating Diagram mapping files")
        provider_resolver.get_mapping_validator(DiagramType.VISIO, [get_data(diagram_mapping_file)]).validate()

    if otm_file:
        logger.info("Validating OTM file")
        OtmValidator().validate(OtmFileLoader().load(otm_file))


@cli.command()
@click.option(IAC_TYPE_NAME, IAC_TYPE_SHORTNAME, help=IAC_TYPE_DESC,
              type=click.Choice(IAC_TYPE_SUPPORTED, case_sensitive=False), required=True
              )
@click.option('--query', '-q', help='JMESPath query to run against the IaC file.')
@click.argument(SOURCE_FILE_NAME, required=True, nargs=-1)
def search(iac_type, query, source_file):
    """
    Searches source files for the given query
    """
    logger.info("Running JMESPath search query against the IaC file")
    get_iac_searcher(iac_type, [get_data(sf) for sf in source_file]).search(query)


@cli.command()
@click.option('--port', '-p', default=5000, envvar='STARTLEFT_PORT', help='Startleft deployment port.')
def server(port: int):
    """
    Launches the REST server to generate OTMs from requests
    """
    configure_logging(verbose=True)
    logger.info(f'Startleft version: {version}')

    fastapi_server.run_webapp(port)


if __name__ == '__main__':
    cli(None, None)
