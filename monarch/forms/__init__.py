from marshmallow import Schema, fields


class SearchSchema(Schema):
    keyword = fields.Str(description="关键字")
    query_field = fields.Str(description="查询字段")


class PaginationSchema(Schema):
    page = fields.Int(required=True, description="第几页")
    per_page = fields.Int(required=True, description="每页数量")


class SortSchema(Schema):
    sort = fields.Int(description="序号")
    sort_field = fields.Str(description="排序字段")


class DateSchema(Schema):
    start = fields.Int(description="开始时间")
    end = fields.Int(description="结束时间")
