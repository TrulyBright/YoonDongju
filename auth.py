import os
import sqlite3
from enum import Enum, IntEnum
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()

class Role(IntEnum):
    user = 0
    board = 1
    president = 2

class User:
    def __init__(self, user_id, username, role, real_name):
        self.id = user_id
        self.username = username
        self.role = role
        self.real_name = real_name

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    @property
    def is_mod(self):
        return Role[self.role] >= Role.board

@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect("sql/users.db") as DB:
        query = "SELECT id, username, role, real_name FROM users WHERE id=?"
        fetched = DB.execute(query, [int(user_id)]).fetchone()
        if fetched:
            return User(fetched[0], fetched[1], fetched[2], fetched[3])
        return None

def setup_auth(app: Flask):
    login_manager.init_app(app)
    load_dotenv()
    app.secret_key = os.getenv("SECRET_KEY")