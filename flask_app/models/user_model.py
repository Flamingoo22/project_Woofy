from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask_app.models import post_model, likes_model
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class User:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.username = db_data['username']
        self.dob = db_data['dob']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        
    
    @classmethod
    def create(cls,data):
        query = '''
                INSERT INTO users (username, dob, email, password)
                VALUES (%(username)s, %(dob)s, %(email)s, %(password)s);
                '''
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = '''
                UPDATE users
                SET users.username = %(username)s, users.dob = %(dob)s
                WHERE users.id = %(id)s;
                '''
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def show_all(cls):
        query = '''
                SELECT *
                FROM users
                '''
        results =  connectToMySQL(DATABASE).query_db(query)
        if not results:
            return False
        users = []
        for user_db in results:
            users.append(cls(user_db))
        return users
    
    @classmethod
    def show_one(cls, data):
        query = '''
                SELECT *
                FROM users
                WHERE users.id = %(id)s;
                '''
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        user = cls(result[0])
        return user
    
    @classmethod
    def get_user_posts(cls, data):
        query = '''
                SELECT *
                FROM users
                LEFT JOIN posts
                ON posts.user_id = users.id
                WHERE users.id = %(id)s
                ORDER BY posts.created_at DESC;
                '''
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        data_row = results[0]
        user_instance = cls(data_row)
        posts = []
        for posts_data in results:
            post_data= {
                **posts_data,
                "id":posts_data['posts.id'],
                'created_at':posts_data['posts.created_at'],
                'updated_at':posts_data['posts.updated_at']
            }
            comments = post_model.Post.get_comments({"id":posts_data['posts.id']})
            post_instance = post_model.Post(post_data)
            
            post_instance.comments = comments
            post_instance.liked_by = likes_model.Like.liked_users({"id":posts_data['posts.id']}) 
            post_instance.num_likes = post_model.Post.num_likes({"id":posts_data['posts.id']})[0]['num_likes']
            post_instance.num_comments = post_model.Post.num_comments({"id":posts_data['posts.id']})[0]['num_comments']
            posts.append(post_instance)
        user_instance.posts = posts
        return user_instance
    
    
    @classmethod
    def find_user_by_id(cls, data):
        query = '''
                SELECT *
                FROM users
                WHERE users.id = %(id)s;
                '''
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        user = cls(result[0])
        return user


    @classmethod
    def find_user_by_username(cls, data):
        query = '''
                SELECT *
                FROM users
                WHERE users.username = %(username)s;
                '''
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        user = cls(result[0])
        return user
    
    @classmethod
    def find_user_by_email(cls, data):
        query = '''
                SELECT *
                FROM users
                WHERE users.email = %(email)s;
                '''
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        user = cls(result[0])
        return user
    
    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['username']) <= 3:
            flash('Username cannot be empty','err_users_username')
            is_valid = False
        elif User.find_user_by_username({'username':data['username']}):
            flash('Username already existed','err_users_repeated_username')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", 'err_users_invalid_email')
            is_valid = False
        elif User.find_user_by_email({'email':data['email']}):
            flash('email already existed','err_users_repeated_email')
            is_valid = False
        if len(data['dob']) <= 2:
            flash('Please specify your date of birth','err_users_dob')
            is_valid = False
        if len(data['password']) < 8:
            flash('Minimum password length is 8','err_users_password')
            is_valid = False
        if not data['password'] == data['confirm_password']:
            flash('password doesnot match','err_users_confirm_password')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid User Information!", 'err_users_login_invalid')
            is_valid = False
        elif not User.find_user_by_email({'email':data['email']}):
            flash("Invalid User Information!", 'err_users_login_invalid')
            is_valid = False
        if len(data['password']) <= 0:
            flash("Invalid User Information!", 'err_users_login_invalid')
            is_valid = False
        if is_valid:
            potential_user = User.find_user_by_email({'email':data['email']})
            if not bcrypt.check_password_hash(potential_user.password, data['password']):
                flash("Invalid User Information!", 'err_users_login_invalid')
                is_valid = False
            else:
                session["uuid"] = potential_user.id
        return is_valid