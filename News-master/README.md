[![codebeat badge](https://codebeat.co/badges/7e2ae46e-24c4-41af-8f4c-b49226560e3a)](https://codebeat.co/projects/github-com-mutugiii-news-master)
# News
## Description
This is an application that displays various News sources and articles from various globally reknown sources. Users can search for respective sources or articles or keywords.
It is a python-flask application that consumes the News API
### By Mutugi

## Setup/Installation Requirements

### Prerequisites
* python3.6
* pip
* Virtual environment(virtualenv)

## Cloning and running
Clone the application using git clone(this copies the app onto your device). In terminal:
```
  $ git clone https://github.com/mutugiii/News/
  $ cd News
```
## Creating the virtual environment
```
  $ python3.6 -m venv --without-pip virtual
  $ source virtual/bin/env
  $ curl https://bootstrap.pypa.io/get-pip.py | python
```
## Installing Flask and other Modules
```
  $ python3.6 -m pip install Flask
  $ python3.6 -m pip install Flask-Bootstrap
  $ python3.6 -m pip install Flask-Script
```
##  Run the application:
```
  $ chmod a+x start.sh
  $ ./start.sh
 ```
## Testing the Application
To run the tests for the class files:
```
 $ python3.6 manage.py test
```
## Technologies Used
* Python 3.6
* Flask

## Behaviour driven development/ User Stories
- User enters the site
- User can view sources and trending articles
- User can see all articles linked to a source
- User can search for articles and sources


### Contact details
Feel free to reach out to the developer via email

## License
[MIT License](https://github.com/Mutugiii/News/blob/master/LICENSE)
