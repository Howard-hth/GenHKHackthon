from flask import Flask
from controllers.api_controller import api
from helpers.scrape import scraper
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    scraper()
    return "Data loaded and cleaned!"

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
