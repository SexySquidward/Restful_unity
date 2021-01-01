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
    Created_by = db.Column(db.Integer, index=True,nullable=False)
    Server_id = db.Column(db.Integer, index=True,nullable=False)
    game_code = db.Column(db.Integer, index=True,nullable=False)
    def __init__(self, createdID, ServerID):
        self.Created_by = createdID
        self.Server_id = ServerID
        self.game_code = Generate_code()
    def json(self):
        return {'GameCode':self.game_code}
class Server_table(db.Model):
    __tablename__ = 'Server_table'
    id = db.Column(db.Integer, primary_key=True)
    Server_name = db.Column(db.String(100), index=True,nullable=False)
    Port = db.Column(db.Integer,index=True,nullable=False)
class FindGame(Resource):
    def get(self, GameCode):
        code = Test_game.query.filter_by(game_code=GameCode).first()
        if code is not None:
            server = Server_table.query.filter_by(id=code.Server_id).first()
            if server is not None:
                return {'Port':server.Port}
            else:
                return {'401':'couldnt find server'}

        else:
            return {'404':'game not found'}

class CreateGame(Resource):
    def post(self,id):
        if id is not None:
            server = Server_table.query.all()
            if server is not None:
                chooseServer = random.choice(server)
                Game = Test_game(createdID=id,ServerID=chooseServer.id)
                db.session.add(Game)
                db.session.commit()
                return Game.json()
            else:
                return {'405':'no servers available'}
        else:
            return {'404':'Couldnt get id'}

def Generate_code():
    value = random.randint(10000,90000)
    return value

api.add_resource(FindGame,'/User/FindGame/<string:GameCode>', methods=['GET'])
api.add_resource(CreateGame,'/User/AddGame/<string:id>')
if __name__ == "__main__":
    app.run('0.0.0.0', port=80)
