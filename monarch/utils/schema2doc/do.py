from functools import wraps
from typing import Union, Type

from flask import request
from marshmallow import Schema, ValidationError

from monarch.utils.schema2doc import for_swagger
from monarch.exc import codes
from monarch.utils.api import biz_success

TYPES_PY = {
    "integer": int,
    "string": str,
    "boolean": bool,
    "number": float,
    "void": None
}


def _get_or_create_schema(
    schema: Union[Schema, Type[Schema]], many: bool = False
) -> Schema:
    if isinstance(schema, Schema):
        return schema
    return schema(many=many)


def merge(first: dict, second: dict) -> dict:
    return {**first, **second}


def _document_like_marshal_with(
    values, status_code: int = 200, description: str = None
):
    description = description or "Success"

    def inner(func):
        doc = {"responses": {status_code: (description, values)}, "__mask__": True}
        func.__apidoc__ = merge(getattr(func, "__apidoc__", {}), doc)
        return func

    return inner


def _check_deprecate_many(many: bool = False):
    if many:
        import warnings

        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "The 'many' parameter is deprecated in favor of passing these "
            "arguments to an actual instance of Marshmallow schema (i.e. "
            "prefer @responds(schema=MySchema(many=True)) instead of "
            "@responds(schema=MySchema, many=True))",
            DeprecationWarning,
            stacklevel=3,
        )


def schema_to_doc(api, query_schema, schema, location="values"):
    """将 marshmallow 的 schema 转换成 flask-restful 能识别的doc

    Args:
        query_schema: marshmallow 的 schema 实例 query_strings
        schema: marshmallow 的 schema 实例 body Schema(many=True)
        api: flask_restplus namespace
        many: schema many
        location: http数据来源 query, header, formData, body, cookie, json, 默认为query
    """

    _parser = api.parser()

    if query_schema:
        for field_name in query_schema.declared_fields:
            field = query_schema.fields[field_name]
            doc_type = field.__class__.__name__.lower()
            params = {
                "location": field.metadata.get("location") or location,
                "type": TYPES_PY[doc_type],
                "name": field.name,
                "required": field.required,
                "help": field.metadata.get("description")
            }
            _parser.add_argument(**params)
    if schema:
        body = for_swagger(
            schema=schema,
            api=api,
            operation="load",
        )
        params = {"expect": [body, _parser]}
        return api.doc(**params)
    elif _parser:
        return api.expect(_parser)


def form_validate(schema):
    """接口请求参数验证"""

    def wrapper(view):
        @wraps(view)
        def view_wrapper(*args, **kw):
            try:
                r_params = request.args if request.method == "GET" else (request.json or {})
                data = schema.load(r_params)
            except ValidationError as ex:
                errors = {"schema_errors": ex.messages}
                return biz_success(
                    code=codes.CODE_BAD_REQUEST,
                    http_code=codes.CODE_BAD_REQUEST,
                    data=errors,
                )

            request.data = data
            return view(*args, **kw)

        return view_wrapper

    return wrapper


def expect(api=None,
           query_schema: Union[Schema, Type[Schema], None] = None,
           schema: Union[Schema, Type[Schema], None] = None
           ):
    """类似flask-restful的expect"""
    def wrapper(view):
        view = schema_to_doc(api, query_schema, schema)(view)
        return form_validate(schema)(view)

    return wrapper


def response_schema_to_doc(schema, many, api, status_code, description):
    _check_deprecate_many(many)

    schema = _get_or_create_schema(schema, many=many)
    api_model = for_swagger(
        schema=schema, api=api, operation="dump"
    )
    if schema.many is True:
        api_model = [api_model]

    inner = _document_like_marshal_with(
        api_model, status_code=status_code, description=description,
    )
    return inner


def response_validate(schema, validate):
    def wrapper(view):
        @wraps(view)
        def view_wrapper(*args, **kw):
            # TODO: response schema validate
            # 正常情况下 为了省事 不要开启 特别是python语言的动态类型
            return view(*args, **kw)

        return view_wrapper

    return wrapper


def response(
    schema=None,
    many: bool = False,
    api=None,
    status_code: int = 200,
    description: str = None,
    validate: bool = False
):
    def wrapper(view):
        view = response_schema_to_doc(schema, many, api, status_code, description)(view)
        return response_validate(schema, validate)(view)
    return wrapper
