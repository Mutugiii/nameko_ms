import os
import jwt
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime, timedelta
from flask import json, Response, request, g
from .models.UserModel import User

load_dotenv()

class Auth():
  '''
  Authentication class to handle token methods
  '''

  @staticmethod
  def generate_token(user_id):
    '''
    Function to generate Token
    '''    
    try:
      payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user_id
      }
      return {
        'status': 'success',
        'token': jwt.encode(
          payload,
          os.environ.get("FLASK_JWT_SECRET_KEY"),
          algorithm='HS256'
        )
      } 
    except Exception as e:
      return {
        'status': 'fail',
        'message': 'error in generating user token',
        'error': str(e)
        }

  @staticmethod
  def decode_token(token):
    '''
    Function to decode jwt token
    '''
    res = {
      'data': {},
      'error': {}
    }
    try:
      payload = jwt.decode(token, os.environ.get('FLASK_JWT_SECRET_KEY'), algorithms=['HS256'])
      res['data'] = {
        'user_id': payload['sub']
      }
      return res
    except jwt.ExpiredSignatureError:
      res['error'] = {
        'message': 'Token Expired, refresh token'
      }
      return res
    except jwt.InvalidTokenError:
      res['error'] = {
        'message': 'Invalid token, use new token'
      }
      return res


  @staticmethod
  def auth_required(func):
    '''
    Decorator to check if user has auth access
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
      auth_header = request.headers.get('Authorization')
      if auth_header:
        auth_token = auth_header.split(" ")[1]
      else:
        return Response(
          mimetype="application/json",
          response=json.dumps({
            'status': 'fail',
            'message': 'Authentication token not found'
            }),
          status=400
        )
      data = Auth.decode_token(auth_token)
      if data['error']:
        return Response(
          mimetype="application/json",
          response=json.dumps({
            'status': 'fail',
            'error': data['error'],
            'message': 'Error decoding token'
            }),
          status=400
        )

      user_id = data['data']['user_id']
      user = User.get_single_user(user_id)
      if not user:
        return Response(
          mimetype="application/json",
          response=json.dumps({
            'status': 'fail',
            'message': 'User does not exist, invalid token'
            }),
          status=400
        )
      
      g.user = {
        'id': user_id
      }
      return func(*args, **kwargs)
    return wrapper


  @staticmethod
  def admin_required(func):
    '''
    Decorator class to check if the user is admin
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
      user = User.get_single_user(g.user.get('id'))
      if user.is_admin == False:
        return Response(
          mimetype="application/json",
          response=json.dumps({
            'status': 'fail',
            'message': 'User does not have admin rights'
            }),
          status=400
        )

      return func(*args, **kwargs)
    return wrapper