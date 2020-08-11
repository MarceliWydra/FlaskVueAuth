from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from flask_restplus import Resource

from server import db, api, jwt
from server.models import User, ExpiredToken, Logs



auth_blueprint = Blueprint('auth', __name__)

@api.route('/api/login')
class Login(Resource):
    def post(self):
        if not request.is_json:
            return make_response(jsonify({"msg": "Wrong request format"}), 400)
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username or not password:
            return make_response(jsonify({"msg": "Missing username or password"}), 400)
        token = User.auth(username=username, password=password)
        if token:
            return make_response(jsonify({"access_token": token}), 200)
        return make_response(jsonify({"msg": "Try again!"}), 400)

@api.route('/api/logs')
class LogsApi(Resource):

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        logs = Logs.get_user_logs(user_id=user_id)
        return make_response(jsonify({"data": logs}), 200)


@api.route('/api/logout')
class LogoutApi(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        resp = ExpiredToken.save_expired_token(jti)
        return make_response(jsonify({'data': resp}), 200)


login_view = Login.as_view('login')
logs_view = LogsApi.as_view('logs')
logout_view = LogoutApi.as_view('logout')
auth_blueprint.add_url_rule(
    '/api/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/api/logs',
    view_func=logs_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/api/logout',
    view_func=logout_view,
    methods=['POST']
)


