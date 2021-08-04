import logging
logger = logging.getLogger(__name__)

import click
from startleft import app

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
        logging.basicConfig(format='%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s', level=level)
    else:
        logging.basicConfig(format='%(message)s', level=level)

@click.group()
@click.option('--log-level', '-l', callback=validate_logging, default='info', help='Set the log level. Must be one of: crit, error, warn, info, debug, none.')
@click.option('--verbose/--no-verbose', default=False, help='Makes logging more verbose.')
#@click.version_option(package_name='startleft')
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
@click.argument('filename', nargs=-1)
def run(type, map, otm, name, id, ir_map, recreate, filename):
    """
    Parses IaC source files into Open Threat Model and immediately uploads threat model to IriusRisk
    """

    iac_to_otm = app.IacToOtmApp(name, id)
    otm_to_ir = app.OtmToIr()

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

    iac_to_otm = app.IacToOtmApp(name, id)
    iac_to_otm.run(type, map, otm, filename)

@cli.command()
@click.option('--ir-map', '-i', multiple=True, help='path to map file')
@click.option('--recreate/--no-recreate', default=False, help='Delete and recreate the product each time')
@click.argument('filename', nargs=-1)
def threatmodel(ir_map, recreate, filename):
    """
    Builds an IriusRisk threat model from OTM files
    """

    otm_to_ir = app.OtmToIr()
    logger.info("Uploading OTM files and generating the IriusRisk threat model")
    otm_to_ir.run(ir_map, recreate, filename)

@cli.command()
@click.option('--map', '-m', multiple=True, help='Map file to validate')
@click.option('--otm', '-o', multiple=True, help='OTM file to validate')
def validate(map, otm):
    """
    Validates a mapping or OTM   file
    """

    if map:
        iac_to_otm = app.IacToOtmApp()
        logger.info("Validating source map file")
        iac_to_otm.validate(map)
        
    if otm:
        otm_to_ir = app.OtmToIr()
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

if __name__ == '__main__':
    cli(None, None)