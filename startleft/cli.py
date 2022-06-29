import logging
import re
import sys

import click

from startleft import messages
from startleft.api.errors import CommonError
from startleft.clioptions.exclusion_option import Exclusion
from startleft.diagram.diagram_type import DiagramType
from startleft.iac.iac_to_otm import IacToOtm
from startleft.iac.iac_type import IacType
from startleft.log import get_log_level, configure_logging
from startleft.messages import *
from startleft.otm.otm_project import OtmProject
from startleft.utils.file_utils import FileUtils
from startleft.version import version

logger = logging.getLogger(__name__)


def validate_server(ctx, param, value):
    regex = "((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}(\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*))?(:[0-9]+)?"
    p = re.compile(regex)

    if value is None or not re.search(p, value):
        raise click.BadParameter("IriusRisk host must follow the convention 'proto://server[:port]'")

    return value


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
        iac_data.append(FileUtils.get_data(iac_file))

    mapping_data = [FileUtils.get_data(mapping_file)]
    otm = OtmProject.from_iac_file_to_otm_stream(project_id, project_name, IacType(iac_type.upper()), iac_data,
                                                 mapping_data)
    otm.otm_to_file(output_file)


def parse_diagram(diagram_type, default_mapping_file, custom_mapping_file, output_file, project_name,
                  project_id, iac_file):
    """
    Parses diagram source files into Open Threat Model
    """
    logger.info("Parsing diagram source files into OTM")
    type_ = DiagramType(diagram_type.upper())
    file = open(iac_file[0], "r")

    mapping_data_list = [FileUtils.get_data(default_mapping_file)]

    if custom_mapping_file:
        mapping_data_list.append(FileUtils.get_data(custom_mapping_file))

    otm_proj = OtmProject.from_diag_file(project_id, project_name, type_, file, mapping_data_list)
    file.close()
    otm_proj.otm_to_file(output_file)


@cli.command(name='parse')
@click.option(messages.IAC_TYPE_NAME, messages.IAC_TYPE_SHORTNAME,
              type=click.Choice(messages.IAC_TYPE_SUPPORTED, case_sensitive=False),
              help=messages.IAC_TYPE_DESC,
              cls=Exclusion,
              mandatory=True,
              mutually_exclusion=['diagram_type', 'default_mapping_file', 'custom_mapping_file'])
@click.option(DIAGRAM_TYPE_NAME, DIAGRAM_TYPE_SHORTNAME,
              type=click.Choice(messages.DIAGRAM_TYPE_SUPPORTED, case_sensitive=False),
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
        logger.info("Validating IaC mapping files")
        OtmProject.validate_iac_mappings_file([FileUtils.get_data(iac_mapping_file)])

    if diagram_mapping_file:
        logger.info("Validating Diagram mapping files")
        OtmProject.validate_diagram_mappings_file([FileUtils.get_data(diagram_mapping_file)])

    if otm_file:
        logger.info("Validating OTM file")
        OtmProject.load_and_validate_otm_file(otm_file)


@cli.command()
@click.option(messages.IAC_TYPE_NAME, messages.IAC_TYPE_SHORTNAME, help=IAC_TYPE_DESC,
              type=click.Choice(messages.IAC_TYPE_SUPPORTED, case_sensitive=False), required=True
              )
@click.option('--query', '-q', help='JMESPath query to run against the IaC file.')
@click.argument(messages.SOURCE_FILE_NAME, required=True, nargs=-1)
def search(iac_type, query, source_file):
    """
    Searches source files for the given query
    """

    iac_to_otm = IacToOtm(None, None, IacType(iac_type.upper()))
    logger.info("Running JMESPath search query against the IaC file")
    iac_to_otm.search(IacType(iac_type.upper()), query, [FileUtils.get_data(source_file[0])])


@cli.command()
@click.option('--port', '-p', default=5000, envvar='STARTLEFT_PORT', help='Startleft deployment port.')
def server(port: int):
    """
    Launches the REST server to generate OTMs from requests
    """
    configure_logging(verbose=True)
    logger.info(f'Startleft version: {version}')

    from startleft.api import fastapi_server
    fastapi_server.run_webapp(port)


if __name__ == '__main__':
    cli(None, None)
