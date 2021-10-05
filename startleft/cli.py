import logging
import sys

import click

from startleft import app
from startleft.api.errors import CommonError
from startleft.config import paths

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
@click.option('--ir-map', '-i', multiple=True, help='path to IriusRisk map file')
@click.option('--recreate/--no-recreate', default=False, help='Delete and recreate the product each time')
@click.option('--irius-server', default='', envvar='IRIUS_SERVER',
              help='IriusRisk server to connect to (proto://server[:port])')
@click.option('--api-token', default='', envvar='IRIUS_API_TOKEN', help='IriusRisk API token')
@click.argument('filename', nargs=-1)
def run(type, map, otm, name, id, ir_map, recreate, irius_server, api_token, filename):
    """
    Parses IaC source files into Open Threat Model and immediately uploads threat model to IriusRisk
    """

    cf_mapping_files, ir_mapping_files = get_default_mappings(map, ir_map)

    inner_run(type, cf_mapping_files, otm, name, id, ir_mapping_files, recreate, irius_server, api_token, filename)


def inner_run(type, map, otm, name, id, ir_map, recreate, irius_server, api_token, filename):
    iac_to_otm = app.IacToOtmApp(name, id)
    otm_to_ir = app.OtmToIr(irius_server, api_token)

    logger.info("Parsing IaC source files into OTM")
    iac_to_otm.run(type, map, otm, filename)
    logger.info("Uploading OTM files and generating the IriusRisk threat model")
    otm_to_ir.run(ir_map, recreate, [otm])


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

    cf_mapping_files, ir_mapping_files = get_default_mappings(map, {})

    iac_to_otm = app.IacToOtmApp(name, id)
    iac_to_otm.run(type, cf_mapping_files, otm, filename)


@cli.command()
@click.option('--ir-map', '-i', multiple=True, help='path to map file')
@click.option('--recreate/--no-recreate', default=False, help='Delete and recreate the product each time')
@click.option('--irius-server', default='', envvar='IRIUS_SERVER',
              help='IriusRisk server to connect to (proto://server[:port])')
@click.option('--api-token', default='', envvar='IRIUS_API_TOKEN', help='IriusRisk API token')
@click.argument('filename', nargs=-1)
def threatmodel(ir_map, recreate, irius_server, api_token, filename):
    """
    Builds an IriusRisk threat model from OTM files
    """
    cf_mapping_files, ir_mapping_files = get_default_mappings({}, ir_map)

    otm_to_ir = app.OtmToIr(irius_server, api_token)
    logger.info("Uploading OTM files and generating the IriusRisk threat model")
    otm_to_ir.run(ir_mapping_files, recreate, filename)


@cli.command()
@click.option('--map', '-m', multiple=True, help='Map file to validate')
@click.option('--otm', '-o', multiple=True, help='OTM file to validate')
def validate(map, otm):
    """
    Validates a mapping or OTM file
    """

    cf_mapping_files, ir_mapping_files = get_default_mappings(map, {})


    if cf_mapping_files:
        iac_to_otm = app.IacToOtmApp(None, None)
        logger.info("Validating source map file")
        iac_to_otm.validate(cf_mapping_files)
        
    if otm:
        otm_to_ir = app.OtmToIr(None, None)
        logger.info("Validating OTM file")
        otm_to_ir.validate(otm)


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

    iac_to_otm = app.IacToOtmApp(None, None)
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


def get_default_mappings(map, ir_map):
    # If map is empty then we load the default map file
    cf_mapping_files = paths.default_cf_mapping_files
    if len(map) != 0:
        cf_mapping_files = map

    ir_mapping_files = paths.default_ir_map
    if len(ir_map) != 0:
        ir_mapping_files = ir_map

    return cf_mapping_files, ir_mapping_files


def check_external_cf_mapping_file(mapping_file):
    # Add custom mapping provided by customer
    cf_mapping_files = paths.default_cf_mapping_files
    if mapping_file and len(mapping_file.filename) != 0:
        cf_mapping_files = [mapping_file.file]

    return cf_mapping_files

if __name__ == '__main__':
    cli(None, None)
