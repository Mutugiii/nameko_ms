import os
import json
from app import db, create_app
from dotenv import load_dotenv
from unittest import TestCase
from app.models.UserModel import User, UserSchema
from app.models.BlogModel import Blogpost, BlogpostSchema
from mimesis import Generic

load_dotenv()
app = create_app(os.getenv("FLASK_ENV"))

generic = Generic('en')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
blog_schema = BlogpostSchema()
blogs_schema = BlogpostSchema(many=True)

def auth_handler(self, url, data) -> dict:
  return self.client.post(
    url,
    data=json.dumps(data),
    content_type='application/json'
  )

def get_handler(self, url, token) -> dict:
  return self.client.get(
    url,
    headers=dict(
      Authorization='Bearer ' + token
    )
  )

def post_handler(self, url, data, token) -> dict:
  return self.client.post(
    url,
    data=json.dumps(data),
    headers=dict(
      Authorization='Bearer ' + token
    ),
    content_type='application/json'
  )

def put_handler(self, url, data, token) -> dict:
  return self.client.put(
    url,
    data=json.dumps(data),
    headers=dict(
      Authorization='Bearer ' + token
    ),
    content_type='application/json'
  )

def delete_handler(self, url, token) -> dict:
  return self.client.delete(
    url,
    headers=dict(
      Authorization='Bearer ' + token
    )
  )

class TestAuthBlueprint(TestCase):
  '''
  Test class to test the auth blueprint
  '''
  def setUp(self):
    self.client = app.test_client()
    res = auth_handler(self, 'v1/auth/register', {
      "username": "test",
      "email": "test@test.com",
      "password": "test"
    })
    self.auth_token = json.loads(res.data)['token']

  def test_registration(self):
    response = auth_handler(self, 'v1/auth/register', {
      "username": generic.person.name(),
      "email": generic.person.email(),
      "password": generic.person.password()
    })
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['token'])
    self.assertTrue(response.content_type == 'application/json')
    self.assertEqual(response.status_code, 201)
      
  def test_registration_duplicate_email(self):
    response = auth_handler(self, 'v1/auth/register', {
      "username": "test2",
      "email": "test@test.com",
      "password": generic.person.password()
    })
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'User with the email provided already exists, log in')
    self.assertEqual(response.status_code, 400)

  def test_registration_incomplete_credentials(self):
    response = auth_handler(self, 'v1/auth/register', {
      "username": generic.person.name(),
      "email": generic.person.email()
    })
    data = json.loads(response.data)    
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Username, Email and Password are required')
    self.assertEqual(response.status_code, 400)

  def test_login(self):
    response = auth_handler(self, 'v1/auth/login', {
      "email": "test@test.com",
      "password": "test"
    })
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['token'])
    self.assertTrue(response.content_type == 'application/json')
    self.assertEqual(response.status_code, 200)

  def test_login_incomplete_credentials(self):
    response = auth_handler(self, 'v1/auth/login', {
      "email": "test@test.com"
    })
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Email and Password are required to login')
    self.assertEqual(response.status_code, 400)

  def test_login_invalid_credentials(self):
    response = auth_handler(self, 'v1/auth/login', {
      "email": "test@test.com",
      "password": "test123"
    })
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Invalid credentials')
    self.assertEqual(response.status_code, 400)
  
  def test_login_unregistered_user(self):
    response = auth_handler(self, 'v1/auth/login', {
      "email": generic.person.email(),
      "password": generic.person.password()
    })
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'User with the email provided does not exist')
    self.assertEqual(response.status_code, 404)
 
  def test_get_all_users(self):
    user = User.get_user_by_email('test@test.com')
    user.update({
      "is_admin": True
    })
    response = get_handler(self, 'v1/auth/', self.auth_token)
    data = json.loads(response.data)    
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(len(data['users']) > 0)
    self.assertEqual(response.status_code, 200)

  def test_token_protected_routes(self):
    response = get_handler(self, 'v1/auth/', "randombearerstring")
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Error decoding token')
    self.assertEqual(response.status_code, 400)

  def test_admin_protected_route(self):
    response = get_handler(self, 'v1/auth/', self.auth_token)
    data = json.loads(response.data)    
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'User does not have admin rights')
    self.assertEqual(response.status_code, 400)

  def test_get_single_user(self):
    user = User.get_user_by_email('test@test.com')
    user.update({
      "is_admin": True
    })
    response = get_handler(self, f'v1/auth/{user.id}', self.auth_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['user'])
    self.assertEqual(response.status_code, 200)
  
  def test_get_non_existent_user(self):
    user = User.get_user_by_email('test@test.com')
    user.update({
      "is_admin": True
    })
    response = get_handler(self, f'v1/auth/{10000}', self.auth_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'User not found')
    self.assertEqual(response.status_code, 404)

  def test_get_profile(self):
    response = get_handler(self, 'v1/auth/me', self.auth_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['me'])
    self.assertEqual(response.status_code, 200)

  def test_update_profile(self):
    response = put_handler(self, 'v1/auth/me',{
      "username": "test2",
    } , self.auth_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['me']['username'] == 'test2')
    self.assertEqual(response.status_code, 200)

  def test_update_profile_already_existing_email(self):
    auth_handler(self, 'v1/auth/register', {
      "username": "random",
      "email": "random@test.com",
      "password": "test"
    })

    response = put_handler(self, 'v1/auth/me',{
      "email": "random@test.com"
    } , self.auth_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'User with email already exists, cannot update to match that email')
    self.assertEqual(response.status_code, 400)

  def test_update_profile_admin_attr(self):
    response = put_handler(self, 'v1/auth/me',{
      "is_admin": True
    } , self.auth_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Cannot self assign admin role')
    self.assertEqual(response.status_code, 400)
  
  def test_delete_profile(self):
    response = delete_handler(self, 'v1/auth/me', self.auth_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['message'] == 'User Profile deleted')
    self.assertEqual(response.status_code, 200)

  def tearDown(self):
    User.query.delete()
    db.session.commit()





class TestBlogBlueprint(TestCase):
  '''
  Test class to test the blog blueprint
  '''
  def setUp(self):
    self.client = app.test_client()
    user_res = auth_handler(self, 'v1/auth/register', {
      "username": generic.person.name(),
      "email": generic.person.email(),
      "password": generic.person.password(),
    })
    self.user_token = json.loads(user_res.data)['token']
    author_res = auth_handler(self, 'v1/auth/register', {
      "username": generic.person.name(),
      "email": generic.person.email(),
      "password": generic.person.password(),
      "role": "author"
    })
    self.author_token = json.loads(author_res.data)['token']
    admin_res = auth_handler(self, 'v1/auth/register', {
      "username": generic.person.name(),
      "email": generic.person.email(),
      "password": generic.person.password(),
    })
    self.admin_token = json.loads(admin_res.data)['token']
      
    admin = User.get_user_by_email(json.loads(admin_res.data)['user']['email'])
    admin.update({"is_admin": True})


    self.valid_payload = {
      "title": generic.text.word(),
      "contents": generic.text.text()
    }

    self.invalid_payload = {
      "title": generic.text.word(),
    }
    

  def test_create_blog_author(self):
    response = post_handler(self, 'v1/main/', self.valid_payload, self.author_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['message'] == 'Blogpost created successfully')
    self.assertEqual(response.status_code, 201)


  def test_create_blog_admin(self):
    response = post_handler(self, 'v1/main/', self.valid_payload, self.admin_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['message'] == 'Blogpost created successfully')
    self.assertEqual(response.status_code, 201)

  def test_create_blog_reader(self):
    response = post_handler(self, 'v1/main/', self.valid_payload, self.user_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Only authors and admins can publish blogs')
    self.assertEqual(response.status_code, 400)

  def test_create_blog_invalid_payload(self):
    response = post_handler(self, 'v1/main/', self.invalid_payload, self.author_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Blog Title and contents are required')
    self.assertEqual(response.status_code, 400)
  
  def test_get_all_blogs(self):
    post_handler(self, 'v1/main/', self.valid_payload, self.author_token)

    response = get_handler(self, 'v1/main/', self.user_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['blogs'])
    self.assertTrue(len(data['blogs']) == 1)
    self.assertEqual(response.status_code, 200)

  def test_get_single_blog(self):
    res = post_handler(self, 'v1/main/', self.valid_payload, self.author_token)
    blog_id = json.loads(res.data)['blog']['id']
    
    response = get_handler(self, f'v1/main/{blog_id}', self.user_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['blog'])
    self.assertEqual(response.status_code, 200)

  def test_get_single_blog_no_permission(self):
    response = get_handler(self, f'v1/main/100', "randomtoken")
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Error decoding token')
    self.assertEqual(response.status_code, 400)

  def test_get_invalid_blog(self):
    response = get_handler(self, 'v1/main/100', self.user_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Blogpost not found')
    self.assertEqual(response.status_code, 404)

  def test_update_blog(self):
    res = post_handler(self, 'v1/main/', self.valid_payload, self.author_token)
    blog_id = json.loads(res.data)['blog']['id']

    response = put_handler(self, f'v1/main/{blog_id}', {'title': 'news'}, self.author_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['message'] == 'Blogpost updated successfully')
    self.assertTrue(data['blog']['title'] == 'news')
    self.assertEqual(response.status_code, 200)

  def test_update_blog_no_permission(self):
    res = post_handler(self, 'v1/main/', self.valid_payload, self.author_token)
    blog_id = json.loads(res.data)['blog']['id']

    response = put_handler(self, f'v1/main/{blog_id}', {'title': 'news'}, self.user_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Permission to access this resource denied!')
    self.assertEqual(response.status_code, 400)

  def test_update_invalid_blog(self):
    response = put_handler(self, 'v1/main/1000', {'title': 'news'}, self.admin_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Blogpost not found')
    self.assertEqual(response.status_code, 404)

  def test_transfer_blog_ownership(self):
    res = post_handler(self, 'v1/main/', self.valid_payload, self.author_token)
    blog_id = json.loads(res.data)['blog']['id']

    response = put_handler(self, f'v1/main/{blog_id}', {'user_id': 1}, self.author_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Blog ownership cannot be transferred')
    self.assertEqual(response.status_code, 400)

  def test_update_other_author_blog(self):
    author2_res = auth_handler(self, 'v1/auth/register', {
      "username": generic.person.name(),
      "email": generic.person.email(),
      "password": generic.person.password(),
      "role": "author"
    })
    self.author2_token = json.loads(author2_res.data)['token']

    res = post_handler(self, 'v1/main/', self.valid_payload, self.author_token)
    blog_id = json.loads(res.data)['blog']['id']

    response = put_handler(self, f'v1/main/{blog_id}', {'title': 'news'}, self.author2_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Permission to access this resource denied!')
    self.assertEqual(response.status_code, 400)

  def test_admin_update_author_blog(self):
    res = post_handler(self, 'v1/main/', self.valid_payload, self.author_token)
    blog_id = json.loads(res.data)['blog']['id']

    response = put_handler(self, f'v1/main/{blog_id}', {'title': 'news'}, self.admin_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['message'] == 'Blogpost updated successfully')
    self.assertTrue(data['blog']['title'] == 'news')
    self.assertEqual(response.status_code, 200)

  def test_delete_blog(self):
    res = post_handler(self, 'v1/main/', self.valid_payload, self.author_token)
    blog_id = json.loads(res.data)['blog']['id']

    response = delete_handler(self, f'v1/main/{blog_id}', self.author_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['message'] == 'Blogpost deleted successfully')
    self.assertEqual(response.status_code, 200)

  def test_delete_blog_no_permission(self):
    res = post_handler(self, 'v1/main/', self.valid_payload, self.author_token)
    blog_id = json.loads(res.data)['blog']['id']

    response = delete_handler(self, f'v1/main/{blog_id}', self.user_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Permission to access this resource denied!')
    self.assertEqual(response.status_code, 400)

  def test_delete_invalid_blog(self):
    response = delete_handler(self, 'v1/main/1000', self.admin_token)
    data = json.loads(response.data)
    self.assertTrue(data['status'] == 'fail')
    self.assertTrue(data['message'] == 'Blogpost does not exist')
    self.assertEqual(response.status_code, 404)

  def tearDown(self):
    Blogpost.query.delete()
    User.query.delete()
    db.session.commit()
