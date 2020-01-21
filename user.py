from flask_login import UserMixin

from sqldb import get_db,close_db

class User(UserMixin):
    
    def __init__(self,id,name,email,profile_pic="/static/images/default_profile.png",acctype="local",password=None):
        self.id=id
        self.name=name
        self.email=email
        self.profile_pic=profile_pic
        self.type=acctype
        self.password=password
        

    @staticmethod
    def get(email):
        db=get_db()
        user = db.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
        if not user:
            return None
        user=User(user[0],name=user[3],email=user[4],profile_pic=user[5],acctype=user[1],password=user[2])    
        return user

    @staticmethod
    def get_from_id(user_id):
        db=get_db()
        user = db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        if not user:
            return None
        user=User(user[0],name=user[3],email=user[4],profile_pic=user[5],acctype=user[1],password=user[2])    
        return user

    @staticmethod
    def create(name, email, profile_pic="static/images/default_profile.png",acctype="local",password=None):
        db = get_db()
        db.execute(
            "INSERT INTO user (name, email, profile_pic,acctype,password) "
            "VALUES (?, ?, ?,?,?)",
            (name, email, profile_pic,acctype,password),
        )
        db.commit()
        close_db(db)
           