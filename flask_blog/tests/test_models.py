from unittest import TestCase
from app.models.UserModel import User, UserRoleEnum
from app.models.BlogModel import Blogpost
from mimesis import Generic
from app import db

generic = Generic('en')

class TestUserModel(TestCase):
  '''
  Test class to test the User model
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
    self.user.save()
    self.admin.save()

  def test_is_instance(self):
    self.assertIsInstance(self.user, User)
    self.assertIsInstance(self.admin, User)

  def test_init(self):
    self.assertEqual(self.user.username, "test")
    self.assertEqual(self.user.email, "test@test.com")

  def test_save_user(self):
    self.all_users = User.get_all_users()

    self.assertIn(self.user, self.all_users)
    self.assertIn(self.admin, self.all_users)
    
    self.assertTrue(len(self.all_users) == 2)

  def test_observe_defaults(self):
    self.assertEqual(self.user.role, UserRoleEnum.reader)
    self.assertEqual(self.user.is_admin, False)
    self.assertEqual(self.admin.is_admin, True)

  def test_update_user(self):
    self.user.update({
      "username": "test2",
    })
    self.assertEqual(self.user.username, "test2")
    

  def test_delete_user(self):
    self.user.delete()
    self.admin.delete()

    self.all_users = User.get_all_users()
    
    self.assertFalse(self.user in self.all_users)
    self.assertFalse(self.admin in self.all_users)

  def tearDown(self):
    User.query.delete()
    db.session.commit()





class TestBlogModel(TestCase):
  '''
  Test class to test the Blogpost Model
  '''
  def setUp(self):
    self.user = User({
      "username": generic.person.name(),
      "email": generic.person.email(),
      "password": generic.person.password(),
    })
    self.user.save()
    self.blog = Blogpost({
      "title": "Post 1", 
      "contents": "This is Blog 1", 
      "user_id": self.user.id
    })
    self.blog.save()

  def test_is_instance(self):
    self.assertIsInstance(self.blog, Blogpost)

  def test_init(self):
    self.assertEqual(self.blog.title, "Post 1")
    self.assertEqual(self.blog.contents, "This is Blog 1")
    self.assertEqual(self.blog.user_id, self.user.id)

  def test_save_blog(self):
    self.all_blogs = Blogpost.get_all_blogposts()
    self.assertIn(self.blog, self.all_blogs)
    
    self.assertTrue(len(self.all_blogs) == 1)

  def test_update_blog(self):
    self.blog.update({
      "title": "Post 2",
      "contents": "This is Blog 2"
    })
    self.assertEqual(self.blog.title, "Post 2")
    self.assertEqual(self.blog.contents, "This is Blog 2")

  def test_delete_blog(self):
    self.blog.delete()
    self.all_blogs = Blogpost.get_all_blogposts()
    self.assertFalse(self.blog in self.all_blogs)

  def tearDown(self):
    Blogpost.query.delete()
    User.query.delete()
    db.session.commit()
