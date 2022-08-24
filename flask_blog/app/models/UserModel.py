from .. import db, bcrypt
from .BlogModel import BlogpostSchema
from enum import Enum
from datetime import datetime
from marshmallow import fields, Schema
from marshmallow_enum import EnumField

class UserRoleEnum(Enum):
  '''Role Options'''
  author = 'author'
  reader = 'reader'

class User(db.Model):
  """
  User Model Class

  Args:
    db.Model: Connect to the database and define db table
  """

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255), nullable = False)
  email = db.Column(db.String(128), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  profile_pic = db.Column(db.String(), nullable=True, default="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAM1BMVEXk5ueutLfn6eqrsbTp6+zg4uOwtrnJzc/j5earsbW0uby4vcDQ09XGyszU19jd3+G/xMamCvwDAAAFLklEQVR4nO2d2bLbIAxAbYE3sDH//7WFbPfexG4MiCAcnWmnrzkjIRaD2jQMwzAMwzAMwzAMwzAMwzAMwzAMwzAMwzAMwzAMw5wQkHJczewxZh2lhNK/CBOQo1n0JIT74/H/qMV0Z7GU3aCcVPuEE1XDCtVLAhgtpme7H0s1N1U7QjO0L8F7llzGeh1hEG/8Lo7TUmmuSrOfns9xnGXpXxsONPpA/B6OqqstjC6Ax/0ujkNdYQQbKNi2k64qiiEZ+ohi35X+2YcZw/WujmslYewiAliVYrxgJYrdwUmwXsU+RdApUi83oNIE27YvrfB/ZPg8+BJETXnqh9CVzBbTQHgojgiCvtqU9thFJg/CKz3VIMKMEkIXxIWqIpIg2SkjYj+xC816mrJae2aiWGykxRNsW0UwiJghJDljYI5CD8GRiCtIsJxizYUPQ2pzItZy5pcisTRdk/a9m4amtNNfBuQkdVhSaYqfpNTSFGfb9GRIakrE2Pm+GFLaCQPqiu0OpWP+HMPQQcgQMiQprWXNmsVwIjQjYi/ZrhAqNTCgr2gu0Jnz85RSSjso0HkMFZ0YZjKkc26a/jlmh9JiDyDxi9oeorTYAzZkwwoMz19pzj9bnH/GP/+qbchjSGflneWYhtTuKdMOmNKZcJ5TjInQKcYXnESd/jQxy0ENpULTNGOGgxpap/oyw9pbUAqhfx2Dbkhovvfgz4iUzoM9+GlK6/Mh4q29hyC1mwro30hpVVLPF9wYQr71RazOeM5/cw81iBRD+A03aM9/C/obbrKjbYSpCmIVG3qT/Q8oeUo3Rz0IL7vI1tEbCB9pSiu8I/aV8x3Kg/BGWrWp4ZVs0nZfmAoEG4h/61yHYIJiFSl6Q0Vk6tTW1N8kYp8hdOkfHYYMXd2Qft+8CYwqYDSKvqIh+MCF8Wgca2u/cwdgeW3TtuVn6+1oBs3yLo5C2JpK6CvQzGpfUkz9UG/87gCsi5o2LIXolxN0FbwAsjOLEr+YJmXn7iR6N0BCt5p5cMxm7eAsfS+/CACQf4CTpKjzgkvr2cVarVTf96372yut7XLJ1sa7lv6VcfgYrWaxqr3Wlo1S6pvStr22sxOtTNPLzdY3nj20bPP+ejFdJYkLsjGLdtPBEbe/mr2bQKiXWJDroA+vtzc0p9aahuwqHMDYrQEXHEw9jwQl3drMpts9JBU1SdktPe5FBRdJQ6bwXBpa57ib2A8kukQDzMjh++Uo7Fo6Wd02Pkf4fknqoo4HtvAIjsqUcjx6DIPgWCaOML9rKI/oqD9/lgNrn+eF+p7j8tnzHBiR7+kdUGw/+V1Kzkc75mMy6U+FMaxjPibiM1U1uGM+puInHpmALZCgP4pt7i840MV8+0R1zPsRB6UTcqpizncYwZ89syDydfyWCwXB1l8/zRNGWbTG/GHKUm9AkxHMc/EGSk3z2+ArEhPEV5TUBLEvUGFcjEUH80J/jveTGOAJEljJbILWGQT3zRYiwuKsUXN1EEJAzBhRJFll7mBUG7KD8EqPkKekBREaL8hMDZLQSG6AQjtHPYmvTQnX0TtpC1SYCe2YdkkyLP3jj5BSbKiuR585eQhTgoje6yIb0Yb0C+mV6EYvebqw5SDy2WmubogZiF2AVxPC2FpDf8H2Q9QWo6IkjUxTWVEI3WY/wrCeSuqJ+eRWzXR/JXwgVjUMozbCOfoEZiSiKVGepqv5CJ8RyR4D7xBeamqa7z3BJ/z17JxuBPdv93d/a2Ki878MMAzDMAzDMAzDMAzDMF/KP09VUmxBAiI3AAAAAElFTkSuQmCC")
  bio = db.Column(db.String(), nullable=True)
  role = db.Column(db.Enum(UserRoleEnum), nullable = False, default=UserRoleEnum.reader)
  is_admin = db.Column(db.Boolean, nullable=False, default=False)
  created_ts = db.Column(db.DateTime, default=datetime.utcnow)
  modified_ts = db.Column(db.DateTime)
  blogs = db.relationship('Blogpost', backref='users', lazy='dynamic')

  def __init__(self, data):
    """
    Class constructor
    """
    self.username = data.get('username')
    self.email = data.get('email')
    self.password = self.set_password(data.get('password'))
    self.profile_pic = data.get('profile_pic')
    self.bio = data.get('bio')
    self.role = data.get('role')
    self.is_admin = data.get('is_admin')
    self.created_ts = datetime.utcnow()
    self.modified_ts = datetime.utcnow()

  def set_password(self, _password):
    return bcrypt.generate_password_hash(_password, rounds=10).decode("utf-8")

  def verify_password(self, _password):
    return bcrypt.check_password_hash(self.password, _password)

  def save(self):
    '''Function to save user to db'''
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    '''Function to modify user'''
    for key, item in data.items():      
      if key == 'password':
        item = self.set_password(item)
      setattr(self, key, item)
    self.modified_ts = datetime.utcnow()
    db.session.commit()

  def delete(self):
    '''Function to delete user'''
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def get_all_users():
    return User.query.all()

  @staticmethod
  def get_single_user(id):
    return User.query.get(id)

  @staticmethod
  def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
  
  def __repr__(self):
    return f'User {self.id}: {self.username}'



class UserSchema(Schema):
  """
  User Schema
  """
  id = fields.Int(dump_only=True)
  username = fields.Str(required=True)
  email = fields.Email(required=True)
  password = fields.Str(load_only=True)
  profile_pic = fields.Str(required=False)
  bio = fields.Str(required=False)
  role = EnumField(UserRoleEnum, required=False)
  is_admin = fields.Boolean(dump_only=True)
  created_ts = fields.DateTime(dump_only=True)
  modified_ts = fields.DateTime(dump_only=True)
  blogposts = fields.Nested(BlogpostSchema, many=True)
