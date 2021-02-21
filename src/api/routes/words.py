from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_security import auth_token_required
from src.api.models.words import WordsRequestSchema
from src.api.scraping.scraping import BeautifulSoupComponent


class CountWords(Resource):
    @auth_token_required
    def get(self):
        try:
            data = request.get_json()
            words_schema = WordsRequestSchema()
            words_request = words_schema.load(data)
            if not words_request.get('words'):
                return make_response('Words list empty.', 400)
            soup = BeautifulSoupComponent(url=words_request.get('url'))
            result = soup.count_words(words=words_request.get('words'))
            return make_response(jsonify(result))
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
