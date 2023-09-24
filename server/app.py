#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
import ipdb

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
CORS(app)


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)
    
    def patch(self, id):
        record = Plant.query.filter(Plant.id == id).first()
        ipdb.set_trace()
        for attr in request.json:
            setattr(record, attr, request.json[attr])

        db.session.add(record)
        db.session.commit()

        response_dict = record.to_dict()

        return make_response(
            response_dict,
            200
        )

  
# Flask Restful is best suited for returning json with RESTful APIs. @app.route() can return json and html, but is more cumbersome to write and debug than Flask RESTful. Use Flask RESTful if you only intend to return json. 


api.add_resource(Plants, '/plants')


class PlantById(Resource):

    def get(self, id):
        return Plant.query.filter(Plant.id == id).first().to_dict()
    
    
    def patch(self, id):
        record = Plant.query.filter(Plant.id == id).first()
        for attr in request.json:
            setattr(record, attr, request.json[attr])

        db.session.add(record)
        db.session.commit()

        response_dict = record.to_dict()

        return make_response(
            response_dict,
            200
        )
    
    def delete(self, id):
        record = Plant.query.filter(Plant.id == id).first() 
        db.session.delete(record)
        db.session.commit()

        response_dict = {
            "message": "record successfully deleted"
        }

        return make_response(
            response_dict,
            204
        )
    
api.add_resource(PlantById, "/plants/<int:id>")



if __name__ == '__main__':
    app.run(port=5555, debug=True)
