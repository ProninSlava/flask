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
    __tablename__ = 'advs'
    id = Column(Integer, primary_key=True)
    header = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    date = Column(DateTime, server_default=func.now())
    owner = Column(String(50))

Base.metadata.create_all(engine)


class AdvView(MethodView):
    def get(self, name):
        session = Session()
        result = {}
        adv_db = session.query(Adv).all()
        list_user_db = [item.owner for item in adv_db]

        if name not in list_user_db:
            return jsonify({404: 'USER with name is not exist!'})

        else:
            result[name] = []
            all_ = session.query(Adv).filter_by(owner=name).all()

            for i in all_:
                result[name].append({
                    'id': i.id,
                    'header': i.header,
                    'description': i.description,
                    'date': i.date.isoformat(),

                })
            return jsonify(result)


    def post(self):
        session = Session()
        new_adv = Adv(**request.json)
        session.add(new_adv)
        session.commit()
        return jsonify({
            'id': new_adv.id,
            'header': new_adv.header,
            'description': new_adv.description,
            'owner': new_adv.owner,
        })


    def delete(self, adv_id:int):
        session = Session()
        adv_del = session.query(Adv).get(adv_id)
        if adv_del is None:
            return jsonify({404:'ADV with id is not exist!!'})
        session.delete(adv_del)
        session.commit()
        return jsonify({'status': 'success'})


# app.add_url_rule('/adv/<name>/', view_func=AdvView.as_view('adv_get'), methods=['GET'])
# app.add_url_rule('/adv/', view_func=AdvView.as_view('adv'), methods=['POST'])
app.add_url_rule('/adv/<id>/', view_func=AdvView.as_view('adv_del'), methods=['DELETE'])



app.run()