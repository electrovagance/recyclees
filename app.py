import os
from models import setup_db
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from server import AuthError, requires_auth, requires_scope

from models import db, setup_db, Items, Donors, Donees

app = Flask(__name__)


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

#----------------------------------------------------------------------------#
# Item routes
#----------------------------------------------------------------------------#


    # This doesn't need authentication
    @app.route("/api/public/items", methods=["GET"])
    @cross_origin(headers=["Content-Type", "Authorization"])
    def get_items():
        try:
            items = [item.format() for item in Items.query.all()]

            if items is None:
                abort(400)

            return jsonify({
                'success': True,
                'items': items
            }), 200
        except Exception:
            abort(404)


    # Route for signed in donor to see a list of posted items up for donation
    # This needs authentication
    @app.route("/api/public/items/<int:item_id>", methods=["GET"])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get_donors_list_of_items(item_id):
        try:
            query = Items.query.filter(Items.id == item_id).first()
            items = [query.format()]

            print(items)

            if items is None:
                abort(400)

            return jsonify({
                'success': True,
                'items': items
            }), 200
        except Exception:
            abort(404)


    # @app.route("/api/items", method=['POST'])
    # @cross_origin(headers=["Content-Type", "Authorization"])
    # @requires_auth
    # def public():
    #     response = "post a new item"
    #     return jsonify(message=response)


    # @app.route("/api/items/<int:id>", method=['DELETE'])
    # @cross_origin(headers=["Content-Type", "Authorization"])
    # @requires_auth
    # def public(id):
    #     response = "delete item with " + id
    #     return jsonify(message=response)


    # @app.route("/api/items/<int:id>", method=['PATCH'])
    # @cross_origin(headers=["Content-Type", "Authorization"])
    # @requires_auth
    # def public(id):
    #     response = "update a posted item"
    #     return jsonify(message=response)


#----------------------------------------------------------------------------#
# Profile route
#----------------------------------------------------------------------------#


    # This needs authentication
    # @app.route("/api/profile")
    # @cross_origin(headers=["Content-Type", "Authorization"])
    # @requires_auth
    # def private():
    #     response = "Hello from a private endpoint! You need to be authenticated to see this."
    #     return jsonify(message=response)

    # This needs authorization
    # @app.route("/api/private-scoped")
    # @cross_origin(headers=["Content-Type", "Authorization"])
    # @requires_auth
    # def private_scoped():
    #     if requires_scope("read:messages"):
    #         response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
    #         return jsonify(message=response)
    #     raise AuthError({
    #         "code": "Unauthorized",
    #         "description": "You don't have access to this resource"
    #     }, 403)


    @app.errorhandler(401)
    def not_authorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Not authorized"
        }), 401


    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405


    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500


    '''
        Implement error handler for AuthError
        error handler should conform to general task above
    '''
    @app.errorhandler(AuthError)
    def autherror(error):
        print(error)
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
