from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_security import auth_token_required
from src.api.models.labels import LabelsRequestSchema
from src.api.scraping.scraping import BeautifulSoupComponent


class CountLabels(Resource):
    @auth_token_required
    def post(self):
        try:
            data = request.get_json()
            labels_schema = LabelsRequestSchema()
            labels_request = labels_schema.load(data)
            if not labels_request.get('labels'):
                return make_response('Labels list empty.', 400)
            soup = BeautifulSoupComponent(url=labels_request.get('url'))
            result = soup.count_labels(labels=labels_request.get('labels'))
            return make_response(jsonify(result))
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
