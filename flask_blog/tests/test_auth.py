from unittest import TestCase
from app.models.UserModel import User
from app.authentication import Auth
from mimesis import Generic

generic = Generic('en')

class TestAuth(TestCase):
  '''
  Test class to test the Auth class
  '''
  def setUp(self):
    self.user = User({
      "username": generic.person.name(),
      "email": generic.person.email(),
      "password": generic.person.password()
    })
    self.user.save()
    

  def test_encode_token(self):
    self.auth_token = Auth.generate_token(self.user.id)
    # Bytes or dict?
    self.assertIsInstance(self.auth_token["token"].encode(), bytes)

  def test_decode_token(self):
    self.auth_token = Auth.generate_token(self.user.id)
    
    self.assertTrue(Auth.decode_token(self.auth_token["token"] == 1))
