from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model, likes_model, comment_model
from datetime import datetime
import math

class Post:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.content = db_data['content']
        self.user_id = db_data['user_id']
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
    def upload(cls, data):
        query = '''
                INSERT INTO posts(title, content, user_id)
                VALUES(%(title)s, %(content)s, %(user_id)s);
                '''
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def edit(cls, data):
        query = '''
                UPDATE posts
                SET posts.title = %(title)s, posts.content = %(content)s
                WHERE posts.id = %(id)s;
                '''
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = '''
                DELETE 
                FROM posts
                WHERE posts.id = %(id)s;
                '''
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_one(cls, data):
        query = '''
                SELECT *
                FROM posts
                LEFT JOIN users
                ON posts.user_id = users.id
                WHERE posts.id = %(id)s;
                '''
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        data_row = results[0]
        post_instance = cls(data_row)
        user_data= {
            **data_row,
            "id":data_row['users.id'],
            'created_at':data_row['users.created_at'],
            'updated_at':data_row['users.updated_at']
        }
        user_instance = user_model.User(user_data)
        post_instance.creator = user_instance
        return post_instance
    
    @classmethod
    def get_comments(cls, data):
        query = '''
                SELECT *
                FROM comments
                LEFT JOIN posts
                ON comments.post_id = posts.id
                WHERE posts.id = %(id)s;
                '''
        results = connectToMySQL(DATABASE).query_db(query, data)
        comments = []
        if not results:
            return []
        for db_rows in results:
            commentor = user_model.User.find_user_by_id({'id':db_rows['user_id']})
            comment = comment_model.Comment(db_rows)
            comment.commentor = commentor
            comments.append(comment)
        return comments
    
    @classmethod
    def get_likes(cls, data):
        query = '''
                SELECT *
                FROM likes
                LEFT JOIN posts
                ON likes.post_id = posts.id
                WHERE posts.id = %(id)s;
                '''
        results = connectToMySQL(DATABASE).query_db(query, data)
        likes = []
        if not results:
            return False
        for db_rows in results:
            likes.append(likes_model.Like(db_rows).num_likes)
        return likes
    
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
    
    @classmethod
    def get_all(cls):
        query = '''
                SELECT *
                FROM posts
                LEFT JOIN users
                ON posts.user_id = users.id
                LEFT JOIN likes 
                ON likes.post_id = posts.id
                GROUP BY posts.id
                ORDER BY posts.created_at DESC;
                '''
        results = connectToMySQL(DATABASE).query_db(query)
        if not results:
            return []
        posts = []
        for db_rows in results:
            posts_instance = cls(db_rows)
            user_data= {
                **db_rows,
                "id":db_rows['users.id'],
                'created_at':db_rows['users.created_at'],
                'updated_at':db_rows['users.updated_at']
            }
            
            like_data = {
                **db_rows,
                'id':db_rows['likes.id'],
                'user_id':db_rows['likes.user_id'],
                'created_at':db_rows['likes.created_at'],
                'updated_at':db_rows['likes.updated_at']
            }
            
            likes = cls.get_likes({'id':db_rows['id']})
            comments = cls.get_comments({'id':db_rows['id']})
            user_instance = user_model.User(user_data)
            posts_instance.creator = user_instance
            
            posts_instance.liked_by = likes_model.Like(like_data).liked_users({'id':db_rows['id']}) 
            posts_instance.likes = likes
            posts_instance.comments = comments
            posts_instance.num_likes = cls.num_likes({'id':db_rows['id']})[0]['num_likes']
            posts_instance.num_comments = cls.num_comments({'id':db_rows['id']})[0]['num_comments']
            posts.append(posts_instance)
        return posts
    
    @staticmethod
    def validate_upload(data):
        is_valid = True
        if len(data['title']) <=3:
            flash('Title is required', 'err_posts_title')
            is_valid = False
        if len(data['content']) <=3:
            flash('Content Cannot be Empty','err_posts_content')
            is_valid = False
        return is_valid
