from datetime import datetime
from functools import wraps

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.exc import IntegrityError

from monarch.corelibs.store import db
from monarch.corelibs.cache_decorator import cache


class Base(db.Model):

    __abstract__ = True

    @classmethod
    def create(cls, _commit=True, **kwargs):
        obj = cls(**kwargs)
        obj.save(_commit)
        return obj

    def update(self, _commit=True, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        self.save(_commit)
        return self

    @classmethod
    def get(cls, id, exclude_deleted=True):
        query = db.session.query(cls)
        if hasattr(cls, "deleted") and exclude_deleted:
            query = query.filter_by(deleted=False)
        return query.filter_by(id=id).first()

    @classmethod
    def paginate(cls, page, per_page, order=None):
        return cls.query.order_by(order).paginate(page, per_page)

    @classmethod
    def all(cls):
        return cls.query.all()

    def save(self, _commit=True):
        try:
            db.session.add(self)
            if _commit:
                db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise

        _hooks = ("_clean_cache",)
        for each in _hooks:
            if hasattr(self, each) and callable(getattr(self, each)):
                func = getattr(self, each)
                func()

    def delete(self, _hard=False, _commit=True):
        if hasattr(self, "deleted") and _hard is False:
            self.deleted = True
            db.session.add(self)
        else:
            db.session.delete(self)
        if _commit:
            db.session.commit()

        _hooks = ("_clean_cache",)
        for each in _hooks:
            if hasattr(self, each) and callable(getattr(self, each)):
                func = getattr(self, each)
                func()


class TimestampMixin(object):
    created_at = Column(DateTime(), default=datetime.now, comment="创建时间")
    updated_at = Column(
        DateTime(),
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        comment="更新时间",
    )

    deleted = Column(Boolean(), default=False, nullable=False, comment="是否删除")


def model_cache(*args, **kwargs):
    """注意，仅用于单model或单model列表的缓存.
    格式如下:
        单model: User
        单model列表: [User<1>, User<2>]
    原因:
        从缓存拿出的model, 处于与db.session分离状态, 为避免relationship机制出错，需手动进行绑定
    其他说明:
        如直接使用monarch.corelibs.cache_decorator.cache进行缓存，则请避免使用relationship属性
    """
    cache_func = cache(*args, **kwargs)

    def _(f):
        func = cache_func(f)

        @wraps(f)
        def __(*a, **kw):
            r = func(*a, **kw)
            if not r:
                return r

            # 返回r为单model列表
            if isinstance(r, list):
                if r[0] not in db.session:
                    r = [db.session.merge(item, load=False) for item in r]

            # 返回r为单model
            elif r not in db.session:
                r = db.session.merge(r, load=False)
            return r
        return __
    return _
