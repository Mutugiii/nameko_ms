import os
from dotenv import load_dotenv
from flask import request, g, json, Response
from . import main
from .. import rpc
from ..authentication import Auth
from ..models.BlogModel import Blogpost, BlogpostSchema
from ..models.UserModel import User, UserRoleEnum

load_dotenv()

blog_schema = BlogpostSchema()
blogs_schema = BlogpostSchema(many=True)

def custom_response(res, code):
  '''
  Function to return a custom response
  '''
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=code
  )



@main.route('/', methods=['GET'])
@Auth.auth_required
def get_blogs():
  '''
  Function to get all blogposts
  '''
  blogs = Blogpost.get_all_blogposts()
  serialized_blogs = blogs_schema.dump(blogs)
  return custom_response({
    'status': 'success',
    'blogs': serialized_blogs
  }, 200)


@main.route('/', methods=['POST'])
@Auth.auth_required
def create_blog():
  '''
  Function to create a blogpost
  '''
  req = request.get_json()

  if not req.get('title') or not req.get('contents'):
    return custom_response({
      'status': 'fail',
      'message': 'Blog Title and contents are required'
    }, 400)

  try:
    data = blog_schema.load(req)
  except Exception as e:
    return custom_response(e, 400)
  
  current_user = User.get_single_user(g.user.get('id'))
  if current_user.is_admin == True or current_user.role == UserRoleEnum.author:
    data["user_id"] = g.user.get('id')
    blog = Blogpost(data)
    blog.save()
    
    result = rpc.mailer_service.create(
      current_user.email,
      current_user.username,
      f'New blogpost {data["title"]} created'
    )

    serialized_blog = blog_schema.dump(blog)
    return custom_response({
      'status': 'success',
      'message': 'Blogpost created successfully',
      'blog': serialized_blog
    }, 201)

  return custom_response({
    'status': 'fail',
    'message': 'Only authors and admins can publish blogs'
  }, 400)


@main.route('/<int:id>', methods=['GET'])
@Auth.auth_required
def get_blog(id):
  '''
  Function to get a single blogpost by id
  '''
  blog = Blogpost.get_single_blogpost(id)
  if not blog:
    return custom_response({
      'status': 'fail',
      'message': 'Blogpost not found'
    }, 404)
  serialized_blog = blog_schema.dump(blog)
  return custom_response({
    'status': 'success',
    'blog': serialized_blog
  }, 200)


@main.route('/<int:id>', methods=['PUT'])
@Auth.auth_required
def update_blog(id):
  '''
  Function to update a blogpost
  '''
  # Check if resource exists
  blog = Blogpost.get_single_blogpost(id)
  if not blog:
    return custom_response({
      'status': 'fail',
      'message': 'Blogpost not found'
    }, 404)

  # Check if blogpost belongs to user or if user is admin
  current_user = User.get_single_user(g.user.get('id'))
  serialized_blog = blog_schema.dump(blog)  
  if current_user.is_admin == True or serialized_blog.get('user_id') == g.user.get('id'):
    req = request.get_json()
      
    if req.get('user_id'):
      return custom_response({
        'status': 'fail',
        'message': 'Blog ownership cannot be transferred'
      }, 400)

    try:
      data = blog_schema.load(req, partial=True)
    except Exception as e:
      return custom_response(e, 400)

    blog.update(data)

    rpc.mailer_service.create(
      current_user.email,
      current_user.username,
      f'New blogpost {data["title"]} created'
    )

    # Serialize updated data to return as json
    serialized_blog = blog_schema.dump(blog)
    return custom_response({
      'status': 'success',
      'message': 'Blogpost updated successfully',
      'blog': serialized_blog
    }, 200)

  return custom_response({
    'status': 'fail',
    'message': 'Permission to access this resource denied!'
  }, 400)


@main.route('/<int:id>', methods=['DELETE'])
@Auth.auth_required
def delete_blog(id):
  '''
  Function to delete a blogpost
  '''
  blog = Blogpost.get_single_blogpost(id)
  if not blog:
    return custom_response({
      'status': 'fail',
      'message': 'Blogpost does not exist'
    }, 404)   
  
  current_user = User.get_single_user(g.user.get('id'))
  serialized_blog = blog_schema.dump(blog)
  # Check if user has admin rights or is owner of blogpost
  if current_user.is_admin == True or serialized_blog.get('user_id') == g.user.get('id'):
    blog.delete()

    with rpc_proxy('mailer_service') as mailer_rpc:
      mailer_rpc.create(
        current_user.email,
        current_user.username,
        f'Blogpost {serialized_blog["title"]} deleted'
      )

    return custom_response({
      'status': 'success',
      'message': 'Blogpost deleted successfully'
    }, 200)
      
  return custom_response({
    'status': 'fail',
    'message': 'Permission to access this resource denied!'
  }, 400)

