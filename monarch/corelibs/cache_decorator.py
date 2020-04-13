import inspect
from functools import wraps
import time
import re
from monarch.utils.empty import Empty
from monarch.corelibs.mcredis import mc

"""
Usage:
# 单参数情况
@cache('Test:User:dev:%s' % '{user_id}')
def query_result(user_id, pid=13):
    return user_id, pid

# 多参数情况
@cache('Test:User:dev:%s:%s' % ('{user_id}', '{pid}'))
def query_result(user_id, pid=14):
    return user_id, pid

# 按参数顺序拼接key
@cache('Text:User:dev:%s:%s')
def query_result(user_id, pid=15):
    return user_id, pid

# 指定参数的数据类型
@cache('Test:User:%(user_id)d:%(pid)d')
def query_result(user_id, pid=15):
    return user_id, pid

# 使用不同的redis库，或者memcache
@cache('Test:User:%(user_id)d:%(pid)d', mc=CACHE[14])
def query_result2(user_id, pid=15):
    return user_id, pid

# 指定过期时间
@cache('Test:User:%(user_id)d:%(pid)d', expire=3600)
def query_result2(user_id, pid=15):
    return user_id, pid

# 指定refresh进行刷新
print(query_result(user_id=111111, refresh=True))
"""


percent_pattern = re.compile(r"%\w")
brace_pattern = re.compile(r"\{[\w\d\.\[\]_]+\}")

__formaters = {}
registered_keys = set()


def format(text, *a, **kw):
    """
    格式化字符串
    :param text:
    :param a:
    :param kw:
    :return:
    """
    f = __formaters.get(text)
    if f is None:
        f = formater(text)
        __formaters[text] = f
    return f(*a, **kw)


def formater(text):
    """
    生成格式化的具体参数
    >>> format('%s %s', 3, 2, 7, a=7, id=8)
    '3 2'
    >>> format('%(a)d %(id)s', 3, 2, 7, a=7, id=8)
    '7 8'
    >>> format('{1} {id}', 3, 2, a=7, id=8)
    '2 8'
    >>> class Obj: id = 3
    >>> format('{obj.id} {0.id}', Obj(), obj=Obj())
    '3 3'
    >>> class Obj: id = 3
    >>> format('{obj.id.__class__} {obj.id.__class__.__class__} {0.id} {1}',
    ...        Obj(), 6, obj=Obj())
    "<type 'int'> <type 'type'> 3 6"
    """
    percent = percent_pattern.findall(text)
    brace = brace_pattern.search(text)
    if percent and brace:
        raise Exception("mixed format is not allowed")

    # 处理 xxx:xxx:%s:%s 的情况
    if percent:
        n = len(percent)
        return lambda *a, **kw: text % tuple(a[:n])

    # 处理xxx:xxx:%(p1)d:%(p2)d 的情况
    elif "%(" in text:
        return lambda *a, **kw: text % kw

    # 处理 xxx:xxx:{p1}:{p2} 的情况
    else:
        return text.format


def gen_key(key_pattern, arg_names, defaults, *a, **kw):
    return gen_key_factory(key_pattern, arg_names, defaults)(*a, **kw)


def gen_key_factory(key_pattern, arg_names, defaults):
    # 将函数的参数和默认值拼接成字典，由于开头的参数有可能没有默认值，所有需要从后往前拼
    args = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}

    # 检查表达式是否可以调用
    if callable(key_pattern):
        names = inspect.getfullargspec(key_pattern)[0]

    def gen_key(*a, **kw):
        aa = args.copy()

        # 更新用户输入的实际参数
        aa.update(zip(arg_names, a))
        aa.update(kw)

        # 将表达式格式化成字符串
        if callable(key_pattern):
            key = key_pattern(*[aa[n] for n in names])
        else:
            key = format(key_pattern, *[aa[n] for n in arg_names], **aa)
        return key and key.replace(" ", "_"), aa

    return gen_key


def cache(key_pattern, expire=0, max_retry=0):
    """
    缓存使用的装饰器
    """

    def deco(f):
        registered_keys.add((key_pattern, f.__doc__ or None))

        # 解析函数的所参数
        arg_names, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, ann = inspect.getfullargspec(
            f
        )

        # 不支持包含*args或者**kwargs参数的函数
        if varargs or varkw:
            raise Exception("do not support var_args")

        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)

            # 判断是否需要进行刷新
            refresh = kw.pop("refresh", False)
            r = mc.get(key) if not refresh else None

            # anti miss-storm
            retry = max_retry
            while r is None and retry > 0:
                if mc.add(key + "#mutex", 1, int(max_retry * 0.1)):
                    break
                time.sleep(0.1)
                r = mc.get(key)
                retry -= 1

            # 缓存没有数据时，调用函数获取数据并刷新缓存
            if r is None:
                r = f(*a, **kw)
                if r is not None:
                    mc.set(key, r, expire)
                if max_retry > 0:
                    mc.delete(key + "#mutex")

            if isinstance(r, Empty):
                r = None
            return r

        _.original_function = f
        return _

    return deco


def delete_cache(key_pattern):
    def deco(f):
        arg_names, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, ann = inspect.getfullargspec(
            f
        )
        if varargs or varkw:
            raise Exception("do not support var_args")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            r = f(*a, **kw)
            mc.delete(key)
            return r

        return _

    return deco
