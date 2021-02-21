from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_security import auth_token_required
from src.api.models.labels import LabelsRequestSchema
from src.api.scraping.scraping import BeautifulSoupComponent


class CountLabels(Resource):
    @auth_token_required
    def post(self):
        """
        Generates the labels count given a URL
        ---
        tags:
            - scraping
        description: Given a URL and a list of labels, using beautifulsoup, traverses the html tree counting labels occurrences
        parameters:
            - in: body
              name: url
              required: true
              type: string
              description: Page URL.
              example: https://www.google.com/
            - in: body
              name: labels
              required: true
              type: array
              description: List of labels.
              example: [h1, div, a, p]
        responses:
            200:
                description: Parameters were valid and the result was returned
            400:
                description: Either some parameters are missing or labels list is empty
            401:
                description: User is not authorized to access the endpoint
        """
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
