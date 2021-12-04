# -*- coding: utf-8 -*-
def handler(doc):
    import json
    from chalice import Blueprint

    swagger_blueprint = Blueprint(__name__)
    @swagger_blueprint.route(doc.root_uri_relative(slashes=True))
    def swagger_blueprint_doc_handler():
        return doc.doc_html

    if doc.editor:
        @swagger_blueprint.route(doc.editor_uri_relative(slashes=True))
        def swagger_blueprint_editor_handler():
            return doc.editor_html

    @swagger_blueprint.route(doc.swagger_json_uri_relative)
    def swagger_blueprint_config_handler():
        return json.dumps(doc.get_config(swagger_blueprint.current_request.path))

    doc.app.register_blueprint(swagger_blueprint)


def match(doc):
    try:
        import chalice
        if isinstance(doc.app, Chalice):
            return handler
    except ImportError:
        pass
    return None