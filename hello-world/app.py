import os

from flask import Flask, request
from flask_smorest import Api
from resources.hello import blp
from db import db
from sqlalchemy import create_engine
from dotenv import load_dotenv

import models

def create_app():
    app = Flask(__name__)
    
    load_dotenv()
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    IP = os.getenv("IP")
    PORT = os.getenv("PORT")
    DB = os.getenv("DB")
    # This engine just used to query for list of databases
    mysql_engine = create_engine(f"mysql://{USER}:{PASSWORD}@{IP}:{PORT}/{DB}")

    # Query for existing databases
    existing_databases = mysql_engine.execute("SHOW DATABASES;")
    # Results are a list of single item tuples, so unpack each tuple
    existing_databases = [d[0] for d in existing_databases]
    database = "test"
    # Create database if not exists
    if database not in existing_databases:
        mysql_engine.execute("CREATE DATABASE {0}".format(database))
        print("Created database {0}".format(database))
        

    
    app.config["PROPOGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Hello World"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/"
    app.config["SQLALCHEMY_DATABASE_URI"] = (f"mysql+pymysql://{USER}:{PASSWORD}@{IP}:{PORT}/{DB}")
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    conn = engine.connect()
    conn.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    db.init_app(app)
    api = Api(app)
    
    
    @app.before_first_request
    def create_tables():
        print("creating tables", flush=True)
        db.create_all()
    
        
    api.register_blueprint(blp)
    return app


