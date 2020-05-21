# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from flask import current_app, Flask, redirect, url_for


def create_app(config, debug=False, testing=False, config_overrides=None):
    application = Flask(__name__)
    application.config.from_object(config)

    application.debug = debug
    application.testing = testing

    if config_overrides:
        application.config.update(config_overrides)

    # Configure logging
    if not application.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with application.app_context():
        model = get_model()
        model.init_app(application)

    # Register the Bookshelf CRUD blueprint.
    from .crud import crud
    application.register_blueprint(crud, url_prefix='/books')

    # Add a default root route.
    @application.route("/")
    def index():
        return redirect(url_for('crud.list'))

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @application.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return application


def get_model():
    from . import model_cloudsql
    model = model_cloudsql
    return model
