import urllib.request,json
from .models import Source,Article

# Getting api key and base urls
api_key = None
article_base_url = None
source_base_url = None
search_base_url = None
source_article_base_url = None

def configure_request(app):
    global api_key,article_base_url,source_base_url,search_base_url, source_article_base_url
    api_key = app.config['NEWS_API_KEY']
    article_base_url = app.config['ARTICLE_BASE_URL']
    source_base_url = app.config['SOURCE_BASE_URL']
    search_base_url = app.config['SEARCH_BASE_URL']
    source_article_base_url = app.config['SOURCE_ARTICLE_BASE_URL']

def process_articles(article_dictionary):
    '''
    Function to process the resulting dictionary that  json.load creates from an api call

    Args:
        article_dictionary: Resulting dictionary of json.loads function
    '''
    articles_list = []
    for article in article_dictionary:
        author = article.get('author')
        title = article.get('title')
        description = article.get('description')
        url = article.get('url')
        image_url = article.get('urlToImage')
        publishedAt = article.get('publishedAt')
        content = article.get('content')

        if image_url:
            article_object = Article(author,title,description,url,image_url,publishedAt,content)
            articles_list.append(article_object)

    return articles_list


def process_sources(sources_dictionary):
    '''
    Function to process the resulting dictionary that  json.load creates from an api call

    Args:
        sources_dictionary: Resulting dictionary of json.loads function
    '''
    sources_list = []
    for source in sources_dictionary:
        id = source.get('id')
        name = source.get('name')
        description = source.get('description')
        url = source.get('url')
        category = source.get('category')
        language = source.get('language')
        country = source.get('country')

        if url:
            source_object = Source(id,name,description,url,category,language,country)
            sources_list.append(source_object)

    return sources_list


def get_articles(query):
    '''
    Function to get articles based on the topic or keyword
    '''
    article_details = json.loads(urllib.request.urlopen(article_base_url.format(query,api_key)).read())

    article_object = None
    if article_details['articles']:
        article_object = process_articles(article_details['articles'])
    return article_object

def search_articles(query):
    '''
    Function to get articles based on the topic or keyword
    ''' 
    article_details = json.loads(urllib.request.urlopen(search_base_url.format(query,api_key)).read())

    article_object = None
    if article_details['articles']:
        article_object = process_articles(article_details['articles'])
    return article_object

def get_sources():
    '''
    Function to get sources
    '''
    sources_details = json.loads(urllib.request.urlopen(source_base_url.format(api_key)).read())

    sources_object = None
    if sources_details['sources']:
        sources_object = process_sources(sources_details['sources'])
    return sources_object

def get_source_articles(query):
    '''
    Function to get articles belonging to a source
    '''
    source_article_details = json.loads(urllib.request.urlopen(source_article_base_url.format(query,api_key)).read())
    
    source_article_object = None
    if source_article_details['articles']:
        source_article_object = process_articles(source_article_details['articles'])
    return source_article_object
