from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    state = db.Column(db.Boolean)
    is_sensor = db.Column(db.Boolean)
    pos_top = db.Column(db.Integer)
    pos_left = db.Column(db.Integer)
    type = db.Column(db.String(15))

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String())
    quoteeng = db.Column(db.String())
    quotespa = db.Column(db.String())

class AccessLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String())
    time = db.Column(db.DateTime)
    useragent = db.Column(db.String())
    action = db.Column(db.String())
    data = db.Column(db.String())

class ThermostatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    temp = db.Column(db.Float)
    set_temp = db.Column(db.Integer)
    mode = db.Column(db.String())
    is_running = db.Column(db.Boolean)

class EntityHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    type = db.Column(db.String())
    entity_id = db.Column(db.Integer)
    state = db.Column(db.Boolean)

class Data(db.Model):
    date = db.Column(db.DateTime, primary_key=True)
    cost = db.Column(db.Float)
    e = db.Column(db.Float)
    w = db.Column(db.Float)

class DataToday(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True)
    cost = db.Column(db.Float)
    e = db.Column(db.Float)
    w = db.Column(db.Float)