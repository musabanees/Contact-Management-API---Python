import requests
from datetime import datetime
BASE = 'http://127.0.0.1:5000/'

email_list = ['mike_new@gmail.com' , 'hrio@gmail.com']
#------------- POST-----------------
print("Post Request for Contacts")
response = requests.post(BASE + 'Person_Contact' , {'Username':'mike12' , 'Firstname':'Mike' , 'Lastname':'hire', 'Gender':'Male'})
print(response.json())

input()

print("Post Request for Email")
response = requests.post(BASE + 'Person_Email' , {'Username':'mike12' , 'Person_Email':email_list })
print(response.json())
#------------- GET -----------------

input()

print("Get Request for Contacts")

response = requests.get(BASE + 'Person_Contact/mike12')
print(response.json())
input()

print("Get Request for Email")
response = requests.get(BASE + 'Person_Email/mike12')
print(response.json())

#------------- UPDATE / PATCH -----------------

print("PATCH Request for Email")
response = requests.patch(BASE + 'Person_Contact/mike12' , {'Username':'mike1222' })
print(response.json())
input()
#------------- GET -----------------


print("Get Request for Contacts")

response = requests.get(BASE + 'Person_Contact/mike1222')
print(response.json())
input()

print("Get Request for Email")
response = requests.get(BASE + 'Person_Email/mike1222')
print(response.json())

#------------------------------------

print("Delete Request for Contacts")
response = requests.delete(BASE + 'Person_Contact/mike1222')
print(response.json())

input()

print("Get Request for Contacts")

response = requests.get(BASE + 'Person_Contact/mike1222')
print(response.json())
input()

print("Get Request for Email")
response = requests.get(BASE + 'Person_Email/mike1222')
print(response.json())

