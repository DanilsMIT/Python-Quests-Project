from app import db

class User(db.Model):
    #atributos de la tabla
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15),unique = True, nullable = False)
    userpassword = db.Column(db.String(300), nullable = False)

    #constructor
    def __init__(self,username,userpassword):
        self.username = username
        self.userpassword = userpassword
    
    #representar datos
    def __repr__(self):
        return f"<User: {self.username}>"
    
class Quest(db.Model):
    #atributos de la tabla
    id = db.Column(db.Integer, primary_key = True)
    userQuest = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    title = db.Column(db.String(20), nullable = False)
    description = db.Column(db.String(500))
    state = db.Column(db.Boolean, default = False)

    #constructor
    def __init__(self,userQuest,title,description,state=False):
        self.userQuest = userQuest
        self.title = title
        self.description = description
        self.state = state

    #representar datos
    def __repr__(self):
        return f'<Quest: {self.title}>'