import re

from marshmallow import ValidationError
from marshmallow.validate import Validator


class PasswordValidator(Validator):
    def __init__(self):
        self.pattern = r"^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).*$"
        self.length = 8

    def __call__(self, value):
        if not re.match(self.pattern, value) or len(value) < self.length:
            raise ValidationError("密码必须包含包含数字、大小写字母，且至少8位")
