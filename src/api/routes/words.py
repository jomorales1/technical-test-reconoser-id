from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_security import auth_token_required
from src.api.models.words import WordsRequestSchema
from src.api.scraping.scraping import BeautifulSoupComponent


class CountWords(Resource):
    @auth_token_required
    def get(self):
        """
        Generates the word count given a URL
        ---
        tags:
            - scraping
        description: Given a URL and a list of words, using beautifulsoup, traverses the html tree counting words occurrences per html tag
        parameters:
            - in: body
              name: url
              required: true
              type: string
              description: Page URL.
              example: https://www.google.com/
            - in: body
              name: words
              required: true
              type: array
              description: List of words.
              example: [yellow, blue, red]
        responses:
            200:
                description: Parameters were valid and the result was returned
            400:
                description: Either some parameters are missing or words list is empty
            401:
                description: User is not authorized to access the endpoint
        """
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
