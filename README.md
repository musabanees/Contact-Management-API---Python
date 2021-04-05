
# Kindly Read API Documentation Before Running This Project
## This is an API written in Python Flask with SQLAlchemy Database under the strong bridge of Design Patterns<br>
### Following Design Patterns use in this project<br>
   • Singleton<br>
o This is used to create a single instance of database, Flask App.<br><br>
### Coding Files System<br>
• There are total of 3 .py files are used in order to reduce the complexity of switching and increase the understanding of how things are working.<br>
• Index.py contains the Factory and DB Module<br>
• Function.py contains the functions used on this project<br>
• Test.py created to run the endpoints of Apis (Use For testing Purpose)<br>
• Initial Testing is performed for you to check, all sample testing is present in text.py<br><br>
### Project Explanation<br>
• For the Model extension, a new table called Email is created with the foreign key of user name which link the Primary key of the Contact Table, hence a Primary key & Foreign key relation was created in order to updating the existing table, which will be time taking.<br>
• Data Integrity & Data Redundancy is maintained. When a username of Contact Table is updated or deleted, the following changes occur in the Email table .<br><br>
### Relation between 2 tables<br>
• In order to run this project, kindly install all recommended libraries given in requirement.txt<br>
