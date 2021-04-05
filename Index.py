#-------------------------- Libraries --------------------------------
from flask import Flask , request
from flask_restful import Api , Resource , abort ,reqparse,fields , marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from datetime import date
from Functions import Check_Gender_Name , ContactParseRequest, EmailParseRequest, convert_list_to_string
import argparse
import abc
# --------------------------------------------------------------------

request_condition = 'Patch'


Contact_resource_fields = {
    'Username':fields.String,
    'Firstname':fields.String,
    'Lastname':fields.String,
    'Gender': fields.String
}

Email_resource_fields = {
    'Username':fields.String,
    'Person_Email': fields.String
}


# ----------------- SIINGLITON PATTERN FOR CREATING SINGLE INSTANCE OF FLASK AND DATABASE -------------------------
class CreateFlaskApp:

    __instance = None

    @staticmethod
    def getInstance():
        if CreateFlaskApp.__instance == None:
            CreateFlaskApp()
        return CreateFlaskApp.__instance

    def __init__(self):

        if CreateFlaskApp.__instance != None:
            raise Exception("Only single Object is Created..")
        else:
            self.app = Flask(__name__)
            self.api = Api(self.app)
            self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
            self.db = SQLAlchemy(self.app)
            CreateFlaskApp.__instance = self
       
    def create_flask_app(self):
        return self.app , self.api , self.db

flask_obj = CreateFlaskApp.getInstance()
app , api , db = flask_obj.create_flask_app()

# ------------------------------------------------------------------------------------------------------------------


#----------------- CONTACT DB MODELS CLASSES--------------------------
class Contact(db.Model):
    __tablename__ = 'Contact'
    Username = db.Column(db.String(100) , primary_key=True)
    Firstname = db.Column(db.Integer , nullable=False)
    Lastname = db.Column(db.String ,  nullable=False)
    Gender = db.Column(db.String ,  nullable=False)

    def __repr__(self):
        return "Person_Contact(Username={Username} , Firstname={Firstname} , Lastname={Lastname},Gender={Gender} )"

class Email(db.Model):
    __tablename__ = 'Email'
    id = db.Column(db.Integer , primary_key=True)
    Username = db.Column(db.String , db.ForeignKey('Contact.Username') ,nullable=False)
    request = db.relationship("Contact", backref=db.backref("Contact", uselist=False))

    Person_Email = db.Column(db.String ,  nullable=True)

    def __repr__(self):
        return "Person_Contact(Username={Username} , Person_Email={Person_Email})"



# db.create_all()

class Person_Email(Resource):


    def __init__(self):
        request_condition = request.method

    # It Is Use To Serialise The Object
    @marshal_with(Email_resource_fields)
    # GET REQUEST: Get the results from the database
    def get(self , contact_username=None):
        if contact_username is None:
            result = Email.query.all()
        else:
            result = Email.query.filter_by(Username = contact_username).first()
            if not result:
                abort(400 , message='ERROR: Contact Has No Email Found!')
        return result

    @marshal_with(Email_resource_fields)
    def post(self , contact_username=None ):
        args = EmailParseRequest(request_condition).parse_args()
        part_str = convert_list_to_string(args['Person_Email'])
        result = Email.query.filter_by(Username = args['Username']).first()
        if result:
            abort(400 , message='ERROR: Username Is Already Exist!')
        result2 = Email(Username=args['Username'], Person_Email= part_str)
        db.session.add(result2)
        db.session.commit()
        return result2, 200

    @marshal_with(Email_resource_fields)
    def patch(self , contact_username=None):
        args = EmailParseRequest(request_condition).parse_args()
        result = Email.query.filter_by(Username = contact_username).first()
        if not result:
            abort(400 , message='ERROR: Email Does Not Exist!')
        if args['Person_Email']:
            result.Person_Email = args['Person_Email']
            
        db.session.commit()

        return result , 200

 

class Person_Contact(Resource):


    def __init__(self):
        request_condition = request.method

    # It Is Use To Serialise The Object
    @marshal_with(Contact_resource_fields)
    # GET REQUEST: Get the results from the database
    def get(self , contact_username=None):
        if contact_username is None:
            result = Contact.query.all()
        else:
            result = Contact.query.filter_by(Username = contact_username).first()
            if not result:
                abort(400 , message='ERROR: Contact Information Does Not Found!')
        return result

    @marshal_with(Contact_resource_fields)
    def post(self , contact_username=None , contact_email=None):
        args = ContactParseRequest(request_condition).parse_args()
        result = Contact.query.filter_by(Username = args['Username']).first()
        if result:
            abort(400 , message='ERROR: Username Is Already Exist!')
        result = Contact(Username=args['Username'], Firstname=args['Firstname'] , Lastname=args['Lastname'] , Gender=args['Gender'] )
        db.session.add(result)
        db.session.commit()
        return result, 200

    @marshal_with(Contact_resource_fields)
    def patch(self , contact_username=None):
        args = ContactParseRequest(request_condition).parse_args()
        result1 = Contact.query.filter_by(Username = contact_username).first()
        result2 = Email.query.filter_by(Username = contact_username).first()

        if not result1:
            abort(400 , message='ERROR: Contact Information Does Not Exist!')
        if args['Username']:
            result1.Username = args['Username']
            result2.Username = args['Username'] # This Ensures the Integrity of the Database
        if args['Firstname']:
            result1.Firstname = args['Firstname']
        if args['Lastname']:
            result1.Lastname = args['Lastname']
        if args['Gender']:
            result1.Gender = args['Gender']
            
        db.session.commit()

        return result1 , 200

    @marshal_with(Contact_resource_fields)
    def delete(self , contact_username):
        args = ContactParseRequest(request_condition).parse_args()
        result1 = Contact.query.filter_by(Username = contact_username).first()

        if not result1:
            abort(400 , message='ERROR: Contact Information Does Not Exist!')
        Contact.query.filter_by(Username = contact_username).delete()
        Email.query.filter_by(Username = contact_username).delete() # This Ensures the Integrity of the Database, hence if the user is deleted, it deleted from both the tables
        db.session.commit()

        return '' , 200

#------------- SOME IMPORTANT API CALL OPERATIONS ---------------------

# POST OPERATION = http://127.0.0.1:5000/Person_Contact + {Username , Firstname, Lastname, Gender} 
# POST OPERATION = http://127.0.0.1:5000/Person_Email + {Username , email} 

# GET OPERATION = http://127.0.0.1:5000/Person_Contact/Username 
# GET OPERATION = http://127.0.0.1:5000/Person_Email/Username 

# PATCH/UPDATE OPERATION = http://127.0.0.1:5000/Person_Contact/Username  + {Username , Firstname, Lastname, Gender} 
# PATCH/UPDATE OPERATION = http://127.0.0.1:5000/Person_Email/Username  + {Username , Email} 

# DELETE OPERATION = http://127.0.0.1:5000/Person_Contact/Username  + {Username , Firstname, Lastname, Gender} 

#------------------------------------------------------------------


api.add_resource(Person_Contact  ,'/Person_Contact', '/Person_Contact/<contact_username>', '/Person_Contact/<contact_username>/<contact_email>')
api.add_resource(Person_Email  ,'/Person_Email', '/Person_Email/<contact_username>')

if __name__ == '__main__':
    app.run(debug=True)