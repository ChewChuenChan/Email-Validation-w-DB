from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Email:
    db = "emails"

    def __init__(self,data):
        self.id = data['id']
        self.email_address = data['email_address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls,data):
        query = "INSERT INTO emails (email_address, created_at, updated_at ) VALUES ( %(email_address)s , NOW() , NOW());"
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        return result
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails;"
        result = connectToMySQL(cls.db).query_db(query)
        all_email = []
        for row in result:
            all_email.append(cls(row))
        return all_email
    
    @staticmethod
    def validate_email( email ):
        is_valid = True
        query = "SELECT * FROM emails WHERE email_address = %(email_address)s;"
        result = connectToMySQL(Email.db).query_db(query,email)
        if len(result) >=1:
            flash("Email already taken.")
            is_valid = False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(email['email_address']):
            flash("Invalid Email") 
            is_valid = False
        else:
            flash("The email address you entered is valid! Thank you")
            is_valid = True
        return is_valid

    @classmethod
    def remove(cls,data):
        query = "DELETE FROM emails WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)