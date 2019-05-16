from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    permission = db.Column(db.Integer,default=0)
    datetime = db.Column(db.DATETIME, default=datetime.utcnow)
    posts = db.relationship('Post', backref='username', lazy='dynamic')
    comments = db.relationship('Comment', backref='username', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username) 

    def QueryOne(username):
        user = User.query.filter_by(username=username).first()
        return user

    def QueryAll():
        users = User.query.all()
        return users

    def Insert(username, password):
        user = User(username=username, password_hash=password, permission=0)
        db.session.add(user)
        db.session.commit()

    def AdminInsert(username, password):
        user = User(username=username, password_hash=password, permission=1)
        db.session.add(user)
        db.session.commit()

    def Update(username ,password):
        user = User.QueryOne(username)
        user.password_hash = password
        db.session.commit()

    def Delete(username):
        user = User.QueryOne(username)
        db.session.delete(user)
        db.session.commit()

    def checkeditpermission(uid):
        if User.QueryOne(uid).permission == 1:
            return True
        return False

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    content = db.Column(db.CLOB)
    tag =  db.Column(db.String(64))
    datetime = db.Column(db.DATETIME, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='title', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.title)

    def QueryOneID(id):
        post = Post.query.filter_by(id=id).first()
        return post

    def QueryOne(title):
        post = Post.query.filter_by(title=title).first()
        return post

    def QueryAll():
        posts = Post.query.all()
        return posts

    def Insert(title, content, username, tag=None):
        user = User.QueryOne(username)
        post = Post(title=title, content=content, tag=tag, username=user)
        db.session.add(post)
        db.session.commit()

    def Update(title ,content, tag=None, new_title=None):
        post = Post.QueryOne(title)
        post.title = new_title
        post.content = content
        post.tag = tag
        db.session.commit()

    def Delete(title):
        post = Post.QueryOne(title)
        db.session.delete(post)
        db.session.commit()

    class post:
        def __init__(self, post):
            self.id = post.id
            self.title = post.title
            self.content = post.content
            self.tag = post.tag
            self.datetime = post.datetime
            self.author = post.username.username
            self.comments = post.comments.order_by(db.desc(Comment.id))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), index=True, unique=True)
    num = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Tag {}>'.format(self.tag) 

    def QueryOne(tag):
        tag = Tag.query.filter_by(tag=tag).first()
        return tag

    def QueryAll():
        tags = Tag.query.all()
        return tags

    def Insert(tag):
        tag = Tag(tag=tag)
        db.session.add(tag)
        db.session.commit()

    def Update(tag, new_tag):
        tag = Tag.QueryOne(tag)
        tag.tag = new_tag
        db.session.commit()

    def Delete(tag):
        tag = Tag.QueryOne(tag)
        db.session.delete(tag)
        db.session.commit()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(64))
    datetime = db.Column(db.DATETIME, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.username)

    def QueryOnePostUserComment(content, title, username):
        comments = Comment.QueryOnePostUserComments(title, username)
        comment = comments.filter(content==content).first()
        return comment

    def QueryOnePostUserComments(title, username):
        comments = Comment.QueryOnePostComments(title)
        user = User.QueryOne(username)
        comments = comments.filter_by(user_id=user.id)
        return comments

    def QueryOnePostComments(title):
        post = Post.QueryOne(title)
        comments = Comment.query.filter_by(post_id=post.id)
        return comments

    def QueryAll():
        comments = Comment.query.all()
        return comments

    def Insert(content, post_id, username):
        post = Post.QueryOneID(post_id)
        user = User.QueryOne(username)
        comment = Comment(content=content, title=post, username=user)
        db.session.add(comment)
        db.session.commit()
# fail
    def Update(content, title, username, new_content):
        comment = Comment.QueryOnePostUserComment(content, title, username)
        comment.content = new_content
        db.session.commit()
# fail
    def Delete(content, title, username):
        comment = Comment.QueryOnePostUserComment(content, title, username)
        db.session.delete(comment)
        db.session.commit()

