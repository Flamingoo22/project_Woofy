from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model, post_model

class Like:
    def __init__(self,db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.post_id = db_data['post_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        
        
    @classmethod
    def like_post(cls, data):
        query = '''
                INSERT INTO likes(user_id, post_id)
                VALUES (%(user_id)s, %(post_id)s)
                '''
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def remove_like(cls,data):
        query = '''
                DELETE
                FROM likes
                WHERE likes.user_id = %(user_id)s AND likes.post_id = %(post_id)s;
                '''
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def liked_users(cls, data):
        query = '''
                SELECT *
                FROM posts
                LEFT JOIN likes
                ON posts.id = likes.post_id
                LEFT JOIN users
                ON likes.user_id = users.id
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
    def num_likes(cls, data):
        query = '''
                SELECT COUNT(users.id) AS num_likes
                FROM posts
                LEFT JOIN likes
                ON posts.id = likes.post_id
                LEFT JOIN users
                ON likes.user_id = users.id
                WHERE posts.id = %(id)s;
                '''
        return connectToMySQL(DATABASE).query_db(query, data)