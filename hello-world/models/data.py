from db import db 

class DataModel(db.Model):
    __tablename__ = "data"
    
    key = db.Column(db.String(80), primary_key = True)
    value = db.Column(db.String(80), unique = False, nullable = False)

    