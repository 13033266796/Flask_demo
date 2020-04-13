from flask_restplus import Namespace, Resource

from monarch.service.admin.captcha import get_captcha


class CaptchaDto:
    ns = Namespace('captcha', description="验证码接口")


ns = CaptchaDto.ns


@ns.route("")
class Captcha(Resource):
    @ns.doc("获取图形验证码")
    @ns.response(200, "获取图形验证码")
    def get(self):
        """获取图形验证码"""
        return get_captcha()
