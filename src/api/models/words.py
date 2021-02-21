from marshmallow import Schema, fields


class WordsRequestData:
    def __init__(self, url, words=[]):
        self.url = url
        self.words = words

    def __repr__(self):
        return f'<LabelsRequestData {self.url}>'


class WordsRequestSchema(Schema):
    class Meta(Schema.Meta):
        model = WordsRequestData

    url = fields.Url(required=True)
    words = fields.List(fields.String, required=True)
