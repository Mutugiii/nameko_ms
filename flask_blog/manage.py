import os
from dotenv import load_dotenv
from flask.cli import FlaskGroup
from app import create_app

load_dotenv()

app = create_app(os.getenv("FLASK_ENV"))
cli = FlaskGroup(app)

@cli.command('test')
def test():
  '''Run the unit tests.'''
  import unittest
  tests = unittest.TestLoader().discover('tests')
  unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
  cli()
