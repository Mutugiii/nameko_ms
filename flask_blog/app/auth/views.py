from flask import request, g, json, Response
from . import auth
from ..authentication import Auth
from ..models.UserModel import User, UserSchema

user_schema =  UserSchema()
users_schema = UserSchema(many=True)

def custom_response(res, code):
  '''
  Custom Response Function
  '''
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=code
  )



@auth.route('/register', methods=['POST'])
def register():
  '''
  Function to register new users
  '''
  req = request.get_json()

  if not req.get("email") or not req.get('password') or not req.get('username'):
    return custom_response({
      'status': 'fail',
      'message': 'Username, Email and Password are required'
    }, 400)

  try:
    data = user_schema.load(req)
  except Exception as e:
    return custom_response(e, 400)
  
  # Check for existing user
  user_exists = User.get_user_by_email(data.get('email'))
  if user_exists:
    message = {
      'status': 'fail',
      'message': 'User with the email provided already exists, log in'
    }
    return custom_response(message, 400)
  
  user = User(data)
  user.save()
  
  serialized_data = user_schema.dump(user)
 
  get_token = Auth.generate_token(serialized_data.get('id'))

  if get_token['status'] == 'fail':
    return custom_response(get_token, 400)

  get_token.update({"user": serialized_data})

  return custom_response(get_token, 201)


@auth.route('/login', methods=['POST'])
def login():
  '''
  Function to login existing users
  '''
  req = request.get_json()
  
  try:
    data = user_schema.load(req, partial=True)
  except Exception as e:
    return custom_response(e, 400)

  if not data.get("email") or not data.get('password'):
    return custom_response({
      'status': 'fail',
      'message': 'Email and Password are required to login'
    }, 400)

  user = User.get_user_by_email(data.get('email'))

  if not user:
    return custom_response({
      'status': 'fail',
      'message': 'User with the email provided does not exist'
    }, 404)

  if not user.verify_password(data.get('password')):
    return custom_response({
      'status': 'fail',
      'message': 'Invalid credentials'
    }, 400)

  serialized_data = user_schema.dump(user)

  get_token = Auth.generate_token(serialized_data.get('id'))  

  if get_token['status'] == 'fail':
    return custom_response(get_token, 400)

  get_token.update({"user": serialized_data})

  return custom_response(get_token, 200)



@auth.route('/', methods=['GET'])
@Auth.auth_required
@Auth.admin_required
def get_users():
  '''
  Function to get all the users
  '''
  users = User.get_all_users()
  serialized_users = users_schema.dump(users)
  return custom_response({
    'status': 'success',
    'users': serialized_users
  }, 200)


@auth.route('/<int:id>', methods=['GET'])
@Auth.auth_required
@Auth.admin_required
def get_user(id):
  '''
  Function to get a single user
  '''
  user = User.get_single_user(id)
  if not user:
    return custom_response({
      'status': 'fail',
      'message': 'User not found'
    }, 404)

  serialized_user = user_schema.dump(user)
  return custom_response({
    'status': 'success',
    'user': serialized_user
  }, 200)



@auth.route('/me', methods=['GET'])
@Auth.auth_required
def get_profile():
  '''
  Function to get the requesting user's profile
  '''

  user = User.get_single_user(g.user.get('id'))
  if not user:
    return custom_response({
      'status': 'fail',
      'message': 'User profile not found'
    }, 404)
  serialized_user = user_schema.dump(user)
  return custom_response({
    'status': 'success',
    'me': serialized_user
  }, 200)


@auth.route('/me', methods=['PUT'])
@Auth.auth_required
def update_profile():
  '''
  Function to update the requesting user's profile
  '''
  req = request.get_json()

  if req.get('is_admin'):
    return custom_response({
      'status': 'fail',
      'message': 'Cannot self assign admin role'
    }, 400)

  try:
    data = user_schema.load(req, partial=True)
  except Exception as e:
    return custom_response(e, 400)

  if data.get('email') and User.get_user_by_email(data['email']):
    return custom_response({
      'status': 'fail',
      'message': 'User with email already exists, cannot update to match that email'
    }, 400)

  user = User.get_single_user(g.user.get('id'))
  user.update(data)
  serialized_user = user_schema.dump(user)
  return custom_response({
    'status': 'success',
    'me': serialized_user
  }, 200)


@auth.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete_profile():
  '''
  Function to delete the requesting user's profile
  '''
  user = User.get_single_user(g.user.get('id'))
  if not user:
    return custom_response({
      'status': 'fail',
      'message': 'User profile does not exist'
    }, 404)
  
  user.delete()
  return custom_response({
    'status': 'success',
    'message': 'User Profile deleted'
  }, 200)