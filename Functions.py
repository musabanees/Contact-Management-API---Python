import datetime
from datetime import date
from flask_restful import  abort , reqparse
import argparse
import re


def Check_Gender_Name(gender_name):
    if gender_name in ('M' , 'm' ,'F' , 'f'):
        raise argparse.ArgumentTypeError("ERROR: Please Write Full Gender Name Male/Female/Others!")

    if gender_name is None:
        raise argparse.ArgumentTypeError("ERROR: Gender Name Is Required!")

    return str(gender_name)

def Check_Email(person_email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, person_email)):
        return str(person_email)
 
    else:
        raise argparse.ArgumentTypeError("ERROR: Invalid Email Address!")


def ContactParseRequest(request_condition):

    Contact_request_args = reqparse.RequestParser()
    Contact_request_args.add_argument('Username' , type=str , required= False if request_condition == 'Patch' else True)
    Contact_request_args.add_argument('Firstname' , type=str, required= False if request_condition == 'Patch' else True)
    Contact_request_args.add_argument('Lastname' , type=str , required= False if request_condition == 'Patch' else True)
    Contact_request_args.add_argument('Gender' , type=Check_Gender_Name , required= False if request_condition == 'Patch' else True)
    Contact_request_args.add_argument('Person_Email' , type=str , required= False if request_condition == 'Patch' else True)

    return Contact_request_args


def EmailParseRequest(request_condition):

    Email_request_args = reqparse.RequestParser()
    Email_request_args.add_argument('Username' , type=str , required= False if request_condition == 'Patch' else True)
    Email_request_args.add_argument('Person_Email' , type=Check_Email ,action='append', required= False if request_condition == 'Patch' else True)

    return Email_request_args

def convert_list_to_string(value):
    result = ''
    for i in value:
        temp = i + ','
        result = result + temp
    return result
