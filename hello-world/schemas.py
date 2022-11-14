from marshmallow import Schema, fields

class DataSchema(Schema):
    key = fields.Int(required = False)
    value = fields.Str(required = True)
    
