from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model, post_model
from datetime import datetime
import math

class Comment:
    def __init__(self,db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.post_id = db_data['post_id']
        self.content = db_data['content']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        
    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        if delta.days > 0:
            return f'{delta.days} days ago'
        elif (math.floor(delta.total_seconds()/60)) >= 60:
            return f'{math.floor(math.floor(delta.total_seconds() /60)/60)} hours ago'
        elif delta.total_seconds() >= 60:
            return f'{math.floor(delta.total_seconds()/60)} minutes ago'
        else:
            return f'{math.floor(delta.total_seconds())} seconds ago'
        
    
    @classmethod
    def comment(cls, data):
        query = '''
                INSERT INTO comments(user_id, post_id, content)
                VALUES (%(user_id)s, %(post_id)s, %(content)s)
                '''
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def remove_comment(cls,data):
        query = '''
                DELETE
                FROM comments
                WHERE comments.id = %(id)s;
                '''
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def comment_users(cls, data):
        query = '''
                SELECT *
                FROM posts
                LEFT JOIN comments
                ON posts.id = comments.posts_id
                LEFT JOIN users
                ON comments.user_id = users.id
                WHERE posts.id = %(id)s;
                '''
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        users = []
        for db_rows in results:
            user_db = {
                **db_rows,
                'id':db_rows['users.id'],
                'created_at':db_rows['users.created_at'],
                'updated_at':db_rows['users.updated_at']
            }
            users.append(user_model.User(user_db))
        return users
    
    @classmethod
    def num_comments(cls, data):
        query = '''
                SELECT COUNT(users.id) AS num_comments
                FROM posts
                LEFT JOIN comments
                ON posts.id = comments.post_id
                LEFT JOIN users
                ON comments.user_id = users.id
                WHERE posts.id = %(id)s;
                '''
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    @staticmethod
    def validate_upload(data):
        is_valid = True
        if len(data['content']) <=3:
            flash('Content Cannot be Empty','err_comment_content')
            is_valid = False
        return is_valid
