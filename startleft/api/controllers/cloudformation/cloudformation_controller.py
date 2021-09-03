import os
from http.client import BAD_REQUEST

from flask import abort, request, jsonify, make_response
from marshmallow import Schema, fields

from examples import paths
from startleft import cli
from flask import Blueprint

iriusrisk_server = 'http://localhost:8080'

bp = Blueprint("cloudformation", __name__, url_prefix="/api/beta/startleft/")


@bp.route('/cloudformation', methods=['POST'])
def cloudformation():
    errors = CloudformationDto().validate(request.form)
    if errors:
        abort(make_response(jsonify(errors), BAD_REQUEST))

    name = request.form['name']
    id = request.form['id']
    cft_file = [request.files.get('cftFile').stream]

    mapping_files = paths.default_mapping_files
    if request.files.get('mappingFile'):
        mapping_files.append(request.files.get('mappingFile').stream)

    api_token = request.headers.get('api-token')

    cli.inner_run(type='YAML', map=mapping_files, otm='threatmodel.otm', name=name, id=id,
                      ir_map=paths.default_ir_map, recreate=1, server=iriusrisk_server, api_token=api_token,
                      filename=cft_file)

    return {}, 200


class CloudformationDto(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
