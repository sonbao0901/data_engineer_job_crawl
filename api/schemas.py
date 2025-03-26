from marshmallow import Schema, fields

class JobSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    company = fields.Str(required=True)