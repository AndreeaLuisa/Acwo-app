from . import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(150), unique=True)
    level = db.Column(db.String(150))
    parola = db.Column(db.String(150))
    nume=db.Column(db.String(150))
    punctaj = db.Column(db.Integer)
    last_test = db.Column(db.String(150))
 #   clasament=db.relationship('Clasament')

    def __init__(self, username, password, punctaj = 0, nume = 'Echipa',  level = 'team', last_test = ''):
        self.username = username
        self.parola = password
        self.punctaj = punctaj
        self.nume = nume
        self.level = level
        self.last_test = last_test

    def change_name(self, nume):
        self.nume = nume

    def change_points(self, punctaj):
        self.punctaj = punctaj

    def change_last_test(self, new_test):
        self.last_test = new_test

class Penalisation(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    username= db.Column(db.String(150))
    penalizare = db.Column(db.Integer)
    motiv = db.Column(db.String(150))
 #   clasament=db.relationship('Clasament')

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.String(150))
    status = db.Column(db.String(150))
    durata = db.Column(db.Integer)
    intrebari = db.relationship('Intrebari')

    def change_status(self, new_status):
        self.status =  new_status
# class RezultateTest(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     tip = db.Column(db.String(150))
#     time = db.Column(db.String(150))
#     points = db.Column(db.Integer)


class Intrebari(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intrebare = db.Column(db.String)
    raspuns_corect = db.Column(db.String)
    tip_test = db.Column(db.String, db.ForeignKey(Test.id))
    raspunsuri = db.relationship('Raspunsuri')

class Raspunsuri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raspuns1 = db.Column(db.String)
    raspuns2 = db.Column(db.String)
    raspuns3 = db.Column(db.String)
    raspuns4 = db.Column(db.String)
    id_intrebare = db.Column(db.Integer, db.ForeignKey(Intrebari.id))


#class Clasament(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    username_id=db.Column(db.Integer,db.ForeignKey(User.id))
#   loc=db.Column(db.Integer)

#class Pozitie(db.Model):
#    id=db.Column(db.Integer,primary_key=True)
#    pozitie=db.column(db.Integer)

# #    def __init__(self,pozitie=1):
##     #     self.pozitie=pozitie
##     poz=Pozitie.first()
##     poz.pozitie=1

# class Admin(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     numeAdmin = db.Column(db.String(150), unique=True)
#     parolaAdmin = db.Column(db.String(150))
