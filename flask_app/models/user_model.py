from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.__init__ import DATABASE
from flask import flash

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User: # CHANGE PROJECT TO FILE NAME
    def __init__( self , data ): 
        self.id = data['id']        # CHANGE SELF.__ TO MATCH SCHEMA
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, form_data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s );
        """
        user_id =connectToMySQL(DATABASE).query_db(query, form_data)
        return user_id



    @staticmethod
    def validate_user(data):
        print(data)
        is_valid = True
        if len(data['first_name']) == 0:
            flash("First Name cannot be blank.")
            is_valid = False

        if len(data['last_name']) == 0:
            flash("Last Name cannot be blank.")
            is_valid = False

        if len(data['email']) == 0:
            flash("Email cannot be blank.")
            is_valid = False

        if len(data['password']) == 0:
            flash("Password cannot be blank.")
            is_valid = False

        if (data['confirm_password'] != data['password']):
            flash("Password does not match.")
            is_valid = False


        if not EMAIL_REGEX.match(data["email"]):
            flash("Email is invalid")
            is_valid = False
        return is_valid

        
    @staticmethod
    def generate_pass_for_new_user(data):
        pw_hash - projects_controllers.bcrypt.generate_password_hash(data["password"])
        update_form - {
                "first_name" : data['first_name'],
                "last_name"  : data['last_name'],
                "email" : data['email'],
                "password" : data['password'],
            }


    # READ ALL
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if len(results)==0: 
            return False
        found_user = cls(results[0])
        return found_user


    #READ ONE
    @classmethod
    def get_one(cls, id):
        data = {'id': id}
        query = '''
            SELECT * FROM users WHERE id = %(id)s;
        '''
        result = connectToMySQL(DATABASE).query_db(query, data)
        return User(result[0])


    #UPDATE
    @classmethod
    def update(cls, data):
        query = '''
            UPDATE users 
            SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s
            WHERE id = %(id)s;
        '''
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results


    #DELETE
    @classmethod
    def delete(cls, id):
        data = {'id': id}
        query = '''
        DELETE FROM users WHERE id = %(id)s;
        '''
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result