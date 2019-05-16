from flask import render_template, flash, redirect, request, url_for
from flask import make_response
from flask import session

from jinja2 import Template

from app import app
from app.models import *
from app.controllers import *


# env = Environment(autoescape=guess_autoescape,
#                   loader=PackageLoader('mypackage'),
#                   extensions=['jinja2.ext.autoescape'])

@app.template_filter('e1')
def e1(string):
    string.replace('&lt;', '<')
    string.replace('&gt;', '>')
    return string

@app.route('/')
def main():
    posts = Post.QueryAll()
    posts.reverse()
    return render_template('main.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if Login.checkuid():
            return render_template("login_success.html")
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.QueryOne(username)
        if Login.checkPassword(username, password):
            SetSession('uid', username)
            return SetCookie('uid', username ,'login_success.html')
        else:
            return render_template("login_fail.html")

@app.route('/logout')
def logout():
    DelSession('uid')
    return render_template('logout.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pre_password = request.form['pre-password']
        if password == pre_password:
            Register.SaveData(username, password)
            return render_template("register_success.html")
        else:
            return render_template("register_fail.html")


# @app.route('/register/check')
# def register_check():
#     return render_template("register_check.html")

@app.route('/success')
def register_success():
    return render_template("register_success.html")

@app.route('/fail')
def register_fail():
    return render_template("register_fail.html")

from app.models import Post
@app.route('/post/<int:post_id>',methods=['GET','POST'])
def post(post_id):
    if request.method == 'POST':
        if Login.checkuid():
            uid = GetCookie('uid')
            content = request.form['content']
            Comment.Insert(content,post_id, uid)
        else:
            return redirect(url_for('needlogin'))

    post = Post.QueryOneID(post_id)
    post = Post.post(post)
    return render_template("post.html", post=post)

@app.route('/editlist')
def editlist():
    if Login.checkuid():
        return render_template("editor_list.html")
    return redirect(url_for('main'))

@app.route('/edit')
def edit():
    if Login.checkuid():
        uid = GetCookie('uid')
        if User.checkeditpermission(uid):
            return render_template("edit.html")
    return redirect(url_for('permission'))

@app.route('/permission')
def permission():
    return render_template('permission.html')

@app.route('/needlogin')
def needlogin():
    return render_template('need_login.html')

from app.models import Post
@app.route('/SavePost', methods=['Post'])
def save_post():
    title = request.form['title']
    content = request.form['content']
    p = Post.Insert(title,content,GetCookie('uid'))
    return 'success'

@app.route('/PublicPost', methods=['Post'])
def public_post():
    title = request.form['title']
    content = request.form['content']
    return 'success'

