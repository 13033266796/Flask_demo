from flask import request
from flask_restplus import Resource, Namespace

from monarch.forms.admin.user import LoginSchema, SearchUserSchema, UserSchema
from monarch.service.admin.user import login, logout, get_user_list

from monarch.utils.common import check_admin_login
from monarch.utils.schema2doc import expect, response

ns = Namespace("user", description="管理员接口")


@ns.route("")
class UserList(Resource):
    @expect(query_schema=SearchUserSchema(), schema=SearchUserSchema(), api=ns)
    @response(schema=UserSchema(many=True), api=ns, validate=True)
    def get(self):
        """管理员列表"""
        return get_user_list(request.data)


@ns.route("/login")
class Login(Resource):
    @expect(schema=LoginSchema(), api=ns)
    def post(self):
        return login(request.data)


@ns.route("/logout")
class Logout(Resource):
    @check_admin_login
    def post(self):
        """注销"""
        return logout()
