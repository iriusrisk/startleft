import logging
import sys

import click

from startleft.api.errors import CommonError
from startleft.config import paths
from startleft.iac_to_otm import IacToOtm
from startleft.mapping.mapping_file_loader import MappingFileLoader
from startleft.mapping.otm_file_loader import OtmFileLoader
from startleft.otm_to_ir import OtmToIr
from startleft.validators.mapping_validator import MappingValidator
from startleft.validators.otm_validator import OtmValidator

logger = logging.getLogger(__name__)

__version__ = "0.1.0"


def validate_logging(ctx, param, value):
    levels = {
        'none': 100,
        'crit': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }

    if value.lower() in levels:
        return levels[value.lower()]
    raise click.BadParameter(f"Log level must be one of: {', '.join(levels.keys())}")


def configure_logger(level, verbose):
    if verbose:
        logging.basicConfig(format='%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s',
                            level=level)
    else:
        logging.basicConfig(format='%(message)s', level=level)


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
@click.option('--log-level', '-l', callback=validate_logging, default='info',
              help='Set the log level. Must be one of: crit, error, warn, info, debug, none.')
@click.option('--verbose/--no-verbose', default=False, help='Makes logging more verbose.')
@click.version_option(__version__)
def cli(log_level, verbose):
    """
    Parse IaC and other files to the Open Threat Model format and upload them to IriusRisk
    """
    configure_logger(log_level, verbose)


@cli.command()
@click.option('--type', '-t', 
              type=click.Choice(['JSON', 'YAML', 'CloudFormation', 'HCL2', 'Terraform', 'XML'], case_sensitive=False),
              default="JSON",
              help='Specify the source file type.')
@click.option('--map', '-m', multiple=True, help='Map file to use when parsing source files')
@click.option('--otm', '-o', default='threatmodel.otm', help='OTM output file name')
@click.option('--name', '-n', help='Project name')
@click.option('--id', help='Project ID')
@click.option('--recreate/--no-recreate', default=False, help='Delete and recreate the project each time')
@click.option('--irius-server', default='', envvar='IRIUS_SERVER',
              help='IriusRisk server to connect to (proto://server[:port])')
@click.option('--api-token', default='', envvar='IRIUS_API_TOKEN', help='IriusRisk API token')
@click.argument('filename', nargs=-1)
def run(type, map, otm, name, id, recreate, irius_server, api_token, filename):
    """
    Parses IaC source files into Open Threat Model and immediately uploads threat model to IriusRisk
    """

    inner_run(type, map, otm, name, id, recreate, irius_server, api_token, filename)


def inner_run(type, map, otm, name, id, recreate, irius_server, api_token, filename):

    cf_mapping_files = get_default_mappings(map)

    iac_to_otm = IacToOtm(name, id)
    otm_to_ir = OtmToIr(irius_server, api_token)

    logger.info("Parsing IaC source files into OTM")
    iac_to_otm.run(type, cf_mapping_files, otm, filename)
    logger.info("Uploading OTM files and generating the IriusRisk threat model")
    otm_to_ir.run(recreate, otm)


@cli.command()
@click.option('--type', '-t',
              type=click.Choice(['JSON', 'YAML', 'CloudFormation', 'HCL2', 'Terraform', 'XML'], case_sensitive=False),
              default="JSON",
              help='Specify the source file type.')
@click.option('--map', '-m', multiple=True, help='Map file to use when parsing source files')
@click.option('--otm', '-o', default='threatmodel.otm', help='OTM output file name')
@click.option('--name', '-n', help='Project name')
@click.option('--id', help='Project ID')
@click.argument('filename', nargs=-1)
def parse(type, map, otm, name, id, filename):
    """
    Parses IaC source files into Open Threat Model
    """

    mapping_files = get_default_mappings(map, type)

    iac_to_otm = IacToOtm(name, id)
    iac_to_otm.run(type, mapping_files, otm, filename)


@cli.command()
@click.option('--recreate/--no-recreate', default=False, help='Delete and recreate the project each time')
@click.option('--irius-server', default='', envvar='IRIUS_SERVER',
              help='IriusRisk server to connect to (proto://server[:port])')
@click.option('--api-token', default='', envvar='IRIUS_API_TOKEN', help='IriusRisk API token')
@click.argument('filename', nargs=-1)
def threatmodel(recreate, irius_server, api_token, filename):
    """
    Uploads an OTM file to IriusRisk
    """
    otm_to_ir = OtmToIr(irius_server, api_token)
    logger.info("Uploading OTM files and generating the IriusRisk threat model")
    otm_to_ir.run(recreate, filename)


@cli.command()
@click.option('--map', '-m', multiple=True, help='Map file to validate')
@click.option('--otm', '-o', multiple=True, help='OTM file to validate')
def validate(map, otm):
    """
    Validates a mapping or OTM file
    """

    iac_mapping_files = get_default_mappings(map)

    if iac_mapping_files:
        iac_mapping = MappingFileLoader().load(iac_mapping_files)
        MappingValidator().validate(iac_mapping)
        
    if otm:
        otm = OtmFileLoader().load(otm)
        OtmValidator().validate(otm)


@cli.command()
@click.option('--type', '-t', 
              type=click.Choice(['JSON', 'YAML', 'CloudFormation', 'HCL2', 'Terraform', 'XML'], case_sensitive=False),
              default="JSON",
              help='Specify the source file type.')
@click.option('--query', help='JMESPath query to run against source files')
@click.argument('filename', nargs=-1)
def search(type, query, filename):
    """
    Searches source files for the given query
    """

    iac_to_otm = IacToOtm(None, None)
    logger.info("Running JMESPath search query against source files")
    iac_to_otm.search(type, query, filename)


@click.option('--irius-server', default='', envvar='IRIUS_SERVER',
              help='IriusRisk server to connect to (proto://server[:port])')
@click.option('--port', default=5000, envvar='application port',
              help='The port to deploy this application to')
@cli.command()
def server(irius_server: str, port: int):
    """
    Launches the REST server in development mode to test the API
    """
    from startleft.api import fastapi_server
    fastapi_server.initialize_webapp(irius_server)
    fastapi_server.run_webapp(port)


def get_default_mappings(mapping_file: [], type=None):
    if type.upper() == 'HCL2':
        mapping_files = paths.default_tf_aws_mapping_files
    else:
        # If map is empty then we load the default map file
        mapping_files = paths.default_cf_mapping_files

    if mapping_file and len(mapping_file) != 0:
        mapping_files = mapping_file

    return mapping_files


if __name__ == '__main__':
    cli(None, None)
