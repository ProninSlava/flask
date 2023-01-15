from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy import Column,Integer, String, DateTime, create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask('app')

DNS = "postgresql+psycopg2://slava:7548@localhost/flask"
engine = create_engine(DNS)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Adv(Base):
    id = Column(Integer, primary_key=True)
    header = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    date = Column(DateTime, server_default=func.now())
    owner = Column(String(50))




class AdvView(MethodView):
    def get(self):
        pass

    def post(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

app.add_url_rule('/adv/', view_func=AdvView.as_view('advs'), methods=['GET', 'POST', 'PATCH', 'DELETE'])

app.run()