from flask import Flask, request
from flask_restful import Resource,Api
from flask_sqlalchemy import SQLAlchemy
from  random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = "30/08/2002"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Unity:6R872AlLdlMFQp0b@192.168.1.8:3308/Surprise_mechanics'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
class Test_game(db.Model):
    __tablename__ = 'Test_game'
    id = db.Column(db.Integer, primary_key=True)
    Created_by = db.Column(db.String(100), index=True,nullable=False)
    ip_address = db.Column(db.String(64), index=True,nullable=False)
    game_code = db.Column(db.String(10), index=True,nullable=False)
    def __init__(self, createdID):
        self.Created_by = createdID
        self.ip_address = Get_ip()
        self.game_code = Generate_code()
    def json(self):
        return {'GameCode':self.game_code}

class FindGame(Resource):
    def get(self, GameCode):
        code = Test_game.query.filter_by(game_code=GameCode).first()
        if code is not None:
            return {"Ip":code.ip_address}
        else:
            return {'404':'game not found'}

class CreateGame(Resource):
    def post(self,id):
        if id is not None:
            Game = Test_game(createdID=id)
            db.session.add(Game)
            db.session.commit()
            return Game.json()
        else:
            return {'404':'Couldnt get id'}

def Generate_code():
    value = randint(10000,90000)
    return value
def Get_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']
api.add_resource(FindGame,'/User/FindGame/<string:GameCode>', methods=['GET'])
api.add_resource(CreateGame,'/User/AddGame/<string:id>')
if __name__ == "__main__":
    app.run('0.0.0.0', port=80)
