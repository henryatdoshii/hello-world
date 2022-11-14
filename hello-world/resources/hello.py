
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import DataModel
from schemas import DataSchema


blp = Blueprint("data", __name__, description = "hello world")

# return {"value": 'world'}
@blp.route("/hello")
class Hello(MethodView):
    @blp.response(200, DataSchema)
    def get(self):
        print("inside helloo")
        return {"value": 'world'} 

# update the stored value in the database with input provided 
@blp.route("/update")
class Update(MethodView):

    @blp.arguments(DataSchema)
    @blp.response(200, DataSchema)
    def post(self, request_data):   
        payload = {'key': 1}
        request_data.update(payload)
        data = DataModel(**request_data)
        try: 
            print("inside try", flush= True)
            db.session.query(DataModel).filter(DataModel.key == data.key).update(request_data)
            db.session.commit()
        except SQLAlchemyError:
            print("inside except", flush = True)
            abort(500, message="Error occured when inserting data into db")
        return data
        

# return view of database
@blp.route("/value")
class Value(MethodView):
    @blp.response(200, DataSchema)
    def get(self):
        return DataModel.query.get_or_404(1)
    
    
# clean db, return db with default value
@blp.route("/reset")
class Value(MethodView):
    @blp.response(200, DataSchema(many= True))
    def get(self):
        db.session.query(DataModel).delete()
        default = {'key': '1', 'value': 'hello world'}
        data = DataModel(**default)
        db.session.add(data)
        db.session.commit()
        return DataModel.query.all()

        


        
    
    




