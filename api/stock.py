from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.stocks import Stock

stock_api = Blueprint('stock_api', __name__,
                   url_prefix='/api/stocks')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(stock_api)

class StockAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate uid
            ticker = body.get('ticker')
            if ticker is None or len(ticker) < 2:
                return {'message': f'Ticker ID is missing, or is less than 2 characters'}, 210
            
            ''' #1: Key code block, setup USER OBJECT '''
            so = Stock(name=name, 
                      ticker=ticker)
            
            ''' Additional garbage error checking '''
            
            rating = body.get("rating")
            if rating is not None:
                so.rating = rating
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            stock = so.create()
            # success returns json of user
            if stock:
                return jsonify(stock.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format occured'}, 210

    class _Read(Resource):
        def get(self):
            stocks = Stock.query.all()    # read/extract all users from database
            json_ready = [stock.read() for stock in stocks]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')