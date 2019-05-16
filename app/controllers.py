from flask import make_response, render_template

from flask import request
from flask import session



from app.models import User

def GetSession(index):
    return session[index]

def GetAllSession():
    return session

def SetSession(index, value):
    session[index] = value

def DelSession(index):
    session.pop(index, None)

def DelAllSession():
    session.clear()

def GetCookie(index):
    return request.cookies.get(index)

def SetCookie(index, value, page):
    resp = make_response(render_template(page))
    resp.set_cookie(index, value)
    return resp

def DelCookie(index, value, page):
    resp = make_response(render_template(page))
    resp.set_cookie(index,  '', expires=0)
    return resp



class Login(object):
    def checkPassword(username, password):
        user = User.QueryOne(username)
        if user is not None and password == user.password_hash:
            return True
        return False

    def checkLoginSession(uid):
        if uid == GetSession('uid'):
            return True
        return False

    def checkuid():
        uid = GetCookie('uid')
        if 'uid' in GetAllSession():
            if uid == GetSession('uid'):
                return True
        return False

class Register(object):
    def SaveData(username,password):
        User.Insert(username, password)


