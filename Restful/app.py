from flask import Flask
from flask_restful import Resource,Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = "30/08/2002"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Unity:6R872AlLdlMFQp0b@192.168.1.8:3308/Surprise_mechanics'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(100), index=True,nullable=False)
    Username = db.Column(db.String(64), index=True,nullable=False)
    passcode = db.Column(db.String(128), index=True,nullable=False)
    def __init__(self, email,username,passcode):
        self.Email = email
        self.Username = username
        self.passcode = generate_password_hash(passcode)
    def check_password(self, password):
        return check_password_hash(self.passcode,password)

    def json(self):
        return {'Username': self.Username,'Passcode':self.passcode,'ID':self.id}

class Server_table(db.Model):
    __tablename__ = 'Server_table'
    id = db.Column(db.Integer, primary_key=True)
    Server_name = db.Column(db.String(100), index=True,nullable=False)
    Port = db.Column(db.Integer,index=True,nullable=False)
    def __init__(self,Server_name,Port):
        self.Server_name = Server_name
        self.Port = Port
    def json(self):
        return {'Server':self.Server_name,'Port':self.Port}

class add_User(Resource):
    def post(self,Email,Username,Passcode):
        email_check = Users.query.filter_by(Email=Email).first()
        username_check = Users.query.filter_by(Username=Username).first()
        if email_check == None and username_check == None:
            account = Users(email=Email,username=Username,passcode=Passcode)
            db.session.add(account)
            db.session.commit()
            return  account.json()
        elif username_check:
            return {'Username_Taken': "Already in use!"}
        elif email_check:
            return {'Email':'Already in use!'}
        else:
            return {'Account': "Already made!"}
class User_login(Resource):
    def get(self, username,passcode):
        account = Users.query.filter_by(Username=username).first()
        if account is None:
            return {'Account': None}, 404
        elif account.check_password(passcode) and account is not None:
            return account.json()
        else:
            return {'Account': None}, 404
class Server(Resource):
    def post(self,Server_Name,Port):
        PortExist = Server_table.query.filter_by(Port=Port).first()
        if PortExist is None:
            server = Server_table(Server_name=Server_Name, Port=Port)
            db.session.add(server)
            db.session.commit()
            return server.json()
        else:
            return {'Server_err':'Port Exist'}

class Server_Remove(Resource):
    def delete(self, Server_name):
        server = Server_table.query.filter_by(Server_name=Server_name).first()
        if server is not None:
            db.session.delete(server)
            db.session.commit()
            return {'Server_Del': 'Server has been deleted'}
        else:
            return {'Server_err': 'Server wasnt found'}
api.add_resource(add_User,'/User/Add/<string:Email>/<string:Username>/<string:Passcode>')
api.add_resource(User_login, '/User/login/<string:username>/<string:passcode>')
api.add_resource(Server, '/Server/Add/<string:Server_Name>/<int:Port>')
api.add_resource(Server_Remove, '/Server/Remove/<string:Server_Name>')
if __name__ == "__main__":
    app.run('0.0.0.0', port=80)
