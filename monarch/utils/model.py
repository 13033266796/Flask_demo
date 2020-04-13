import base64
import os


class CSPRNG(object):
    """密码学安全随机数生成器（Cryptographically secure pseudorandom number generator），
    用来安全地生成各种 Token。
    random.choice 作为 token 生成器是不够安全的，因为它所使用的是伪随机数生成器，在
    生成数量足够大的情况下数据是可以预测的。
    参考：https://docs.python.org/2/library/random.html
    """

    def __init__(self, length=16):
        """
        :param int length: 要生成的随机数的长度
        """
        self.length = length

    def bytes(self):
        """将随机数作为字节返回
        :rtype: str
        """
        return os.urandom(self.length)

    def hex(self):
        """
        :rtype: str
        """
        return base64.b16encode(os.urandom(self.length))

    def base64(self):
        """将随机字符串进行 urlsafe base64 然后返回
        :rtype: str
        """
        return base64.b64encode(os.urandom(self.length))

    def urlsafe_base64(self):
        """将随机字符串进行 urlsafe base64 然后返回
        :rtype: str
        """
        return base64.urlsafe_b64encode(os.urandom(self.length))

    def encode_as(self, func):
        """使用给定的函数对随机字符串进行编码。
        :param function func: 从 bytes 到 bytes 的函数
        :rtype: str
        """
        return func(os.urandom(self.length))


# http://sqlalchemy-utils.readthedocs.io/en/latest/_modules/sqlalchemy_utils/functions/database.html#escape_like
def escape_like(string, escape_char="\\"):
    """escape the string paremeter used in SQL like expressions"""
    return (
        string.replace(escape_char, escape_char * 2)
        .replace("%", escape_char + "%")
        .replace("_", escape_char + "_")
    )
