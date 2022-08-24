from .. import db
from datetime import datetime
from marshmallow import fields, Schema

class Blogpost(db.Model):
  """
  Blogpost Model class

  Args:
    db.Model: Connect to database and define as db table
  """

  __tablename__ = 'blogposts'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), nullable=False)
  contents = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  created_ts = db.Column(db.DateTime, default=datetime.utcnow)
  modified_ts = db.Column(db.DateTime)

  def __init__(self, data):
    self.title = data.get('title')
    self.contents = data.get('contents')
    self.user_id = data.get('user_id')
    self.created_ts = datetime.utcnow()
    self.modified_ts = datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.modified_ts = datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @staticmethod
  def get_all_blogposts():
    return Blogpost.query.all()
  
  @staticmethod
  def get_single_blogpost(id):
    return Blogpost.query.get(id)

  def __repr__(self):
    return f'Post {self.id}: {self.title}'


class BlogpostSchema(Schema):
  """
  Blogpost Schema
  """
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True)
  contents = fields.Str(required=True)
  user_id = fields.Int(dump_only=True)
  created_ts = fields.DateTime(dump_only=True)
  modified_ts = fields.DateTime(dump_only=True)
