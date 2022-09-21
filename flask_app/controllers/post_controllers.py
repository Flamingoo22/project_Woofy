from flask import render_template, redirect, session, flash, request, jsonify
from flask_app import bcrypt,app
from flask_app.models import user_model, post_model, likes_model, comment_model

@app.route('/dashboard')
def dashboard():
    posts = post_model.Post.get_all()
    return render_template('dashboard.html', posts = posts)

@app.route('/woofy/user_page')
def my_page():
    if 'uuid' not in session:
        return redirect('/woofy/register')
    user = user_model.User.get_user_posts({'id':session['uuid']})
    return render_template('user.html', user = user)

@app.route('/woofy/user_page/<int:user_id>')
def user_page(user_id):
    if 'uuid' not in session:
        return redirect('/woofy/register')
    if user_id == session['uuid']:
        return redirect('/woofy/user_page')
    user = user_model.User.get_user_posts({'id':user_id})
    return render_template('other_users.html', user = user)

'''
***********************************
ACTION ROUTES
***********************************
'''

@app.route('/woofy/user_page/update', methods=['POST'])
def update_post():
    if 'uuid' not in session:
        return redirect('/woofy/register')
    data = {
        **request.form,
    }
    post_model.Post.edit(data)
    return redirect('/woofy/user_page')

@app.route('/comments', methods = ['POST'])
def comment():
    if 'uuid' not in session:
        return redirect('/woofy/register')
    data = {
        'user_id':session['uuid'],
        **request.form
    }
    comment_model.Comment.comment(data)
    return redirect('/dashboard')

'''
************************************
JSONIFY
************************************
'''
@app.route('/woofy/user_page/<int:post_id>')
def post_info(post_id):
    if 'uuid' not in session:
        return redirect('/woofy/register')
    post = post_model.Post.get_one({'id':post_id})
    res = {
        'title':post.title,
        'content':post.content
    }
    return jsonify(res)


@app.route('/comments/delete/<int:comment_id>')
def delete_comment(comment_id):
    if 'uuid' not in session:
        return redirect('/woofy/register')
    data = {
        'id':comment_id,
    }
    comment_model.Comment.remove_comment(data)
    return jsonify()

@app.route('/dashboard/post/create', methods = ['POST'])
def dash_post():
    if 'uuid' not in session:
        return redirect('/woofy/register')
    data = {
        **request.form,
        'user_id':session['uuid']
    }
    creator = user_model.User.show_one({'id': session['uuid']})
    post_id = post_model.Post.upload(data)
    res = {
        'form':data,
        'post_id':post_id,
        'creator':f'{creator.username}'
    }
    return jsonify(res)

@app.route('/posts/delete/<int:post_id>')
def delete(post_id):
    if 'uuid' not in session:
        return redirect('/woofy/register')
    post_model.Post.delete({'id':post_id})
    return jsonify()

@app.route('/dashboard/like/<int:post_id>')
def like(post_id):
    if 'uuid' not in session:
        return redirect('/woofy/register')
    data = {
        'user_id':session['uuid'],
        'post_id':post_id
    }
    likes_model.Like.like_post(data)
    return jsonify()

@app.route('/dashboard/rm_like/<int:post_id>')
def rm_like(post_id):
    if 'uuid' not in session:
        return redirect('/woofy/register')
    data = {
        'user_id':session['uuid'],
        'post_id':post_id
    }
    likes_model.Like.remove_like(data)
    return jsonify()