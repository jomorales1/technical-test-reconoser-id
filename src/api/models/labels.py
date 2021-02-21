from marshmallow import Schema, fields


class LabelsRequestData:
    def __init__(self, url, labels=[]):
        self.url = url
        self.labels = labels

    def __repr__(self):
        return f'<LabelsRequestData {self.url}>'


class LabelsRequestSchema(Schema):
    class Meta(Schema.Meta):
        model = LabelsRequestData

    url = fields.Url(required=True)
    labels = fields.List(fields.String, required=True)
