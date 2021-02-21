from flask import Flask
from flask_restful import Api
from src.api.routes.labels import CountLabels
from src.api.routes.words import CountWords

app = Flask(__name__)
api = Api(app, prefix='/api')

api.add_resource(CountLabels, '/label/count')
api.add_resource(CountWords, '/word/count')

if __name__ == '__main__':
    app.run(debug=True)
