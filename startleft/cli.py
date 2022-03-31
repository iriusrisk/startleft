import logging
import re
import sys

import click

from startleft.api.controllers.iac.iac_type import IacType
from startleft.api.errors import CommonError
from startleft.iac_to_otm import IacToOtm
from startleft.messages import messages
from startleft.project.iriusrisk_project_repository import IriusriskProjectRepository
from startleft.project.otm_project import OtmProject
from startleft.project.otm_project_service import OtmProjectService

logger = logging.getLogger(__name__)

__version__ = "0.1.0"


def get_log_level(ctx, param, value):
    levels = {
        'NONE': 100,
        'CRIT': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARN': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }

    if value.upper() in levels:
        return levels[value.upper()]
    raise click.BadParameter(f"Log level must be one of: {', '.join(levels.keys())}")


def configure_logger(level, verbose):
    if verbose:
        logging.basicConfig(format='%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s',
                            level=level)
    else:
        logging.basicConfig(format='%(message)s', level=level)


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
            sys.exit(e.system_exit_status)
        except Exception as exc:
            logger.exception(exc)


@click.group(cls=CatchAllExceptions)
@click.option('--log-level', '-l',
              type=click.Choice(['CRIT', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'NONE'], case_sensitive=False),
              callback=get_log_level, default='info', help='Set the log level.')
@click.option('--verbose/--no-verbose', '-v/-nv', default=False, help='Makes logging more verbose.')
@click.version_option(__version__)
def cli(log_level, verbose):
    """
    Parse IaC and other files to the Open Threat Model format and upload them to IriusRisk
    """
    configure_logger(log_level, verbose)


@cli.command()
@click.option(messages.IAC_TYPE_NAME, messages.IAC_TYPE_SHORTNAME, type=click.Choice(messages.IAC_TYPE_SUPPORTED, case_sensitive=False), required=True, help=messages.IAC_TYPE_DESC)
@click.option(messages.MAPPING_FILE_NAME, messages.MAPPING_FILE_SHORTNAME, help=messages.MAPPING_FILE_DESC)
@click.option(messages.OUTPUT_FILE_NAME, messages.OUTPUT_FILE_SHORTNAME, default=messages.OUTPUT_FILE, help=messages.OUTPUT_FILE_DESC)
@click.option(messages.PROJECT_NAME_NAME, messages.PROJECT_NAME_SHORTNAME, required=True, help=messages.PROJECT_NAME_DESC)
@click.option(messages.PROJECT_ID_NAME, messages.PROJECT_ID_SHORTNAME, required=True, help=messages.PROJECT_ID_DESC)
@click.option(messages.RECREATE_NAME, messages.RECREATE_SHORTNAME, default=False, help=messages.RECREATE_DESC)
@click.option(messages.IRIUS_SERVER_NAME, messages.IRIUS_SERVER_SHORTNAME, default='', envvar=messages.IRIUS_SERVER_ENVAR, callback=validate_server, help=messages.IRIUS_SERVER_DESC)
@click.option(messages.API_TOKEN_NAME, messages.API_TOKEN_SHORTNAME, default='', envvar=messages.API_TOKEN_ENVAR, help=messages.API_TOKEN_DESC)
@click.argument(messages.IAC_FILE_NAME, required=True, nargs=-1)
def run(iac_type, mapping_file, output_file, project_name, project_id, recreate, irius_server, api_token,
        iac_file):
    """
    Parses an IaC file into an Open Threat Model (OTM) and uploads it to IriusRisk
    """
    logger.info("Parsing IaC source files into OTM")
    otm_project = OtmProject.from_iac_file(project_id, project_name, IacType(iac_type.upper()), iac_file,
                                           mapping_file, output_file)
    otm_service = OtmProjectService(IriusriskProjectRepository(api_token, irius_server))

    __create_or_recreate_otm_project(recreate, otm_service, otm_project)


@cli.command()
@click.option(messages.IAC_TYPE_NAME, messages.IAC_TYPE_SHORTNAME, type=click.Choice(messages.IAC_TYPE_SUPPORTED, case_sensitive=False), required=True, help=messages.IAC_TYPE_DESC)
@click.option(messages.MAPPING_FILE_NAME, messages.MAPPING_FILE_SHORTNAME, help=messages.MAPPING_FILE_DESC)
@click.option(messages.OUTPUT_FILE_NAME, messages.OUTPUT_FILE_SHORTNAME, default=messages.OUTPUT_FILE, help=messages.OUTPUT_FILE_DESC)
@click.option(messages.PROJECT_NAME_NAME, messages.PROJECT_NAME_SHORTNAME, required=True, help=messages.PROJECT_NAME_DESC)
@click.option(messages.PROJECT_ID_NAME, messages.PROJECT_ID_SHORTNAME, required=True, help=messages.PROJECT_ID_DESC)
@click.argument(messages.IAC_FILE_NAME, required=True, nargs=-1)
def parse(iac_type, mapping_file, output_file, project_name, project_id, iac_file):
    """
    Parses IaC source files into Open Threat Model
    """
    logger.info("Parsing IaC source files into OTM")
    OtmProject.from_iac_file(project_id, project_name, IacType(iac_type.upper()), iac_file, mapping_file, output_file)


@cli.command()
@click.option(messages.RECREATE_NAME, messages.RECREATE_SHORTNAME, default=False, help=messages.RECREATE_DESC)
@click.option(messages.IRIUS_SERVER_NAME, messages.IRIUS_SERVER_SHORTNAME, default='', envvar=messages.IRIUS_SERVER_ENVAR, callback=validate_server, help=messages.IRIUS_SERVER_DESC)
@click.option(messages.API_TOKEN_NAME, messages.API_TOKEN_SHORTNAME, default='', envvar=messages.API_TOKEN_ENVAR, help=messages.API_TOKEN_DESC)
@click.argument(messages.IAC_FILE_NAME, required=True, nargs=-1)
def threatmodel(recreate, irius_server, api_token, iac_file):
    """
    Uploads an OTM file to IriusRisk
    """
    otm_project = OtmProject.from_otm_file(iac_file)
    otm_service = OtmProjectService(IriusriskProjectRepository(api_token, irius_server))

    __create_or_recreate_otm_project(recreate, otm_service, otm_project)


@cli.command()
@click.option(messages.MAPPING_FILE_NAME, messages.MAPPING_FILE_SHORTNAME, help=messages.MAPPING_FILE_DESC)
@click.option(messages.OUTPUT_FILE_NAME, messages.OUTPUT_FILE_SHORTNAME, default=messages.OUTPUT_FILE, help=messages.OUTPUT_FILE_DESC)
def validate(mapping_file, output_file):
    """
    Validates a mapping or OTM file
    """
    if mapping_file:
        logger.info("Validating IaC mapping files")
        OtmProject.validate_iac_mappings_file(mapping_file)

    if output_file:
        logger.info("Validating OTM file")
        OtmProject.load_and_validate_otm_file(output_file)


@cli.command()
@click.option(messages.IAC_TYPE_NAME, messages.IAC_TYPE_SHORTNAME, type=click.Choice(messages.IAC_TYPE_SUPPORTED, case_sensitive=False), required=True, help=messages.IAC_TYPE_DESC)
@click.option('--query', '-q', help='JMESPath query to run against the IaC file.')
@click.argument(messages.IAC_FILE_NAME, required=True, nargs=-1)
def search(iac_type, query, iac_file):
    """
    Searches source files for the given query
    """

    iac_to_otm = IacToOtm(None, None, IacType(iac_type.upper()))
    logger.info("Running JMESPath search query against the IaC file")
    iac_to_otm.search(IacType(iac_type.upper()), query, iac_file)


@cli.command()
@click.option('--port', '-p', default=5000, envvar='STARTLEFT_PORT', help='Startleft deployment port.')
def server(port: int):
    """
    Launches the REST server to generate OTMs from requests
    """
    from startleft.api import fastapi_server
    fastapi_server.run_webapp(port)


def __create_or_recreate_otm_project(recreate: bool, otm_service: OtmProjectService, otm_project: OtmProject):
    if recreate:
        logger.info("Uploading OTM files and recreating the IriusRisk threat model")
        otm_service.recreate_project(otm_project)
    else:
        logger.info("Uploading OTM files and generating the IriusRisk threat model")
        otm_service.update_or_create_project(otm_project)


if __name__ == '__main__':
    cli(None, None)
