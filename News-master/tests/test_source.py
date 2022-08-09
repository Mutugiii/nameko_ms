import unittest
from app.models import Source

class TestSource(unittest.TestCase):
    '''
    Test class for source objects

    Args:
        unittest.TestCase: 
    '''
    def setUp(self):
        '''
        To set up before every test
        '''
        self.new_source = Source('abc-news', 'ABC News', 'Your trusted source for breaking news, analysis, exclusive interviews, headlines, and videos at ABCNews.com.', 'https://abcnews.go.com', 'general','en','us')

    def tearDown(self):
        '''
        Tear Down class to clean up after every test case
        '''
        self.new_source = None

    def test_instance(self):
        '''
        Test that the initialized article is an instance of the model class
        '''
        self.assertTrue(isinstance(self.new_source,Source))

    def test_init(self):
        '''
        Test that it is initialized properly
        '''
        self.assertEqual(self.new_source.id,'abc-news')
        self.assertEqual(self.new_source.name, 'ABC News')
        self.assertEqual(self.new_source.description, 'Your trusted source for breaking news, analysis, exclusive interviews, headlines, and videos at ABCNews.com.')
        self.assertEqual(self.new_source.url,'https://abcnews.go.com')
        self.assertEqual(self.new_source.category,'general')
        self.assertEqual(self.new_source.language,'en')
        self.assertEqual(self.new_source.country, 'us')

