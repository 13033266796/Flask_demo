from sqlalchemy import (Column, Integer, String)

from monarch.models.base import Base, TimestampMixin


class Company(Base, TimestampMixin):
    """公司表"""

    __tablename__ = "company"

    Q_TYPE_NAME = "name"
    Q_TYPE_CODE = "code"

    # status
    STATUS_ON = 1  # 启用
    STATUS_OFF = 2  # 禁用

    id = Column(
        Integer(), nullable=False, autoincrement=True, primary_key=True, comment="公司ID",
    )

    code = Column(String(32), nullable=False, comment="公司编码")
    name = Column(String(128), nullable=True, comment="公司名称")
    remark = Column(String(255), nullable=True, comment="企业描述")
    logo = Column(String(255), nullable=True, default=None, comment="企业logo")
