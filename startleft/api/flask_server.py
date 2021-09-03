from flask import Flask

from startleft.api.controllers.cloudformation import cloudformation_controller
from startleft.api.controllers.health import health_controller

webapp = Flask("startleft")


def create_app():
    """Create and configure an instance of the Flask application."""

    # apply the blueprints to the app
    webapp.register_blueprint(health_controller.bp)
    webapp.register_blueprint(cloudformation_controller.bp)

    # register error handler
    from startleft.api import error_handler
    webapp.register_error_handler(Exception, error_handler.handle_exception)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    webapp.add_url_rule("/", endpoint="index")

    return webapp
