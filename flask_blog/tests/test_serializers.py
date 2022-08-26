from unittest import TestCase
from app.models.UserModel import User, UserSchema
from app.models.BlogModel import Blogpost, BlogpostSchema
from mimesis import Generic

generic = Generic('en')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
blog_schema = BlogpostSchema()
blogs_schema = BlogpostSchema(many=True)

class TestUserSchema(TestCase):
  '''
  class to test the userschema serializer class
  '''
  def setUp(self):
    self.user = User({
      "username": "test",
      "email": "test@test.com",
      "password": "test"
    })
    self.admin = User({
      "username": generic.person.name(),
      "email": generic.person.email(),
      "password": generic.person.password(),
      "is_admin": True
    })
    self.serializer = user_schema.dump(self.user)
    self.many_serializer = users_schema.dump([self.user, self.admin])
  
  def test_contains_expected_fields(self):
    self.assertCountEqual(self.serializer.keys(), [
      'id',
      'username',
      'email',
      'profile_pic',
      'bio',
      'role',
      'is_admin',
      'created_ts',
      'modified_ts',
    ])

  def test_field_contents(self):
    self.assertEqual(self.serializer['username'], self.user.username)
    self.assertEqual(self.serializer['email'], self.user.email)
  
  def test_many_serializer(self):
    self.assertEqual(len(self.many_serializer), 2)

  
class TestBlogpostSchema(TestCase):
  '''
  class to test the blogpostschema serializer class
  '''
  def setUp(self):
    self.user = User({
      "username": "test",
      "email": "test@test.com",
      "password": "test"
    })
    self.user.save()
    
    self.blog = Blogpost({
      "title": "Post 1", 
      "contents": "This is Blog 1", 
      "user_id": self.user.id
    })
    self.blog2 = Blogpost({
      "title": "Post 2", 
      "contents": "This is Blog 2", 
      "user_id": self.user.id
    })
    self.serializer = blog_schema.dump(self.blog)
    self.many_serializer = blogs_schema.dump([self.blog, self.blog2])

  def test_contains_expected_fields(self):
    self.assertCountEqual(self.serializer.keys(), [
      'id',
      'title',
      'contents',
      'user_id',
      'created_ts',
      'modified_ts',
    ])

  def test_field_contents(self):
    self.assertEqual(self.serializer['title'], self.blog.title)
    self.assertEqual(self.serializer['contents'], self.blog.contents)

  def test_many_serializer(self):
    self.assertEqual(len(self.many_serializer), 2)

  def tearDown(self):
    self.user.delete()