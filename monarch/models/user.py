from werkzeug.security import generate_password_hash, check_password_hash

from monarch.models.base import Base, TimestampMixin
from sqlalchemy import Column, String, Index, Integer

from monarch.utils.model import escape_like


class User(Base, TimestampMixin):
    """用户表"""
    __tablename__ = "user"

    __table_args__ = (
        # UniqueConstraint('unionid', 'deleted'， name='idx_unionid_deleted'),
        # 唯一索引/唯一性约束
        Index("uq_account_deleted", "account", "deleted", unique=True),
        # 普通索引
        Index("idx_company_id", "company_id"),
    )

    Q_TYPE_ACCOUNT = "account"

    id = Column(
        String(32),
        nullable=False,
        primary_key=True,
        comment="管理员ID",
    )

    company_id = Column(Integer, nullable=False, comment="公司ID")
    account = Column(String(32), nullable=False, comment="账号")
    # password 为 表字段 的名字，实则为了解决赋值时直接将 password 赋值给模型（password字段不存在，所以无法赋值）,为了加密
    _password = Column("password", String(128), nullable=False, default=None, comment="密码")

    @property
    def password(self):
        '''
        getter 函数
        读取 password 字段
        :return:
        '''
        return self._password

    @password.setter
    def password(self, raw):
        '''
         setter 函数
        解决明文存储 password 问题
        设置 password 字段
        :param raw:
        :return:
        '''
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    @classmethod
    def get_by_account(cls, account, deleted=False):
        return cls.query.filter(
            cls.account == account,
            cls.deleted == deleted
        ).first()

    @classmethod
    def paginate_user(cls, query_field, keyword):
        q = []
        if keyword:
            if query_field == User.Q_TYPE_ACCOUNT:
                q.append(cls.account.like("%" + escape_like(keyword) + "%"))

        return cls.query.filter(*q).order_by(cls.created_at.desc())
