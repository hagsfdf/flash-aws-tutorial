import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import hashlib

import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = text.strip(' ')
    return text

def valid_imdb_url(txt):
    x = urlparse(txt)
    if x.netloc != 'www.imdb.com':
        return False
    path = x.path.split('/')
    if path[1] != 'title':
        return False
    if not path[2].startswith('tt'):
        return False
    return True

def crawl_data(url):
    attributes = ['title', 'director', 'releasedDate', 'description', 'imageUrl']
    ret = {row:None for row in attributes}

    try:
        page = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        return e.code

    soup = BeautifulSoup(page, "lxml")

    right_table = soup.find('div', class_='poster')

    imglink = right_table.find('img').get('src')

    ret['imageUrl'] = imglink

    bigStory = soup.find('div', id='titleStoryLine')
    storyline = bigStory.find('div', class_='inline canwrap')
    storyline = storyline.find('span').get_text().strip()
    cleansed_storyline = clean_text(storyline)

    ret['description'] = cleansed_storyline

    titleYear = soup.find('div', class_ = 'title_wrapper').find('h1')

    year = titleYear.find('a').get_text()

    ret['releasedDate'] = year

    title = titleYear.get_text()

    title = title[:title.rfind('(')].strip()

    ret['title'] = title

    director = soup.find('div', class_='credit_summary_item').find('a').get_text()

    ret['director'] = director

    # # Gonna use S3 bucket? Let's comment it for now...
    # bucket = "flaskfosterpic2020"
    # fn = hashlib.sha256(imglink.encode('utf-8')).hexdigest() + '.jpg'
    # urllib.request.urlretrieve(imglink, '/tmp/'+fn)
    # s3 = boto3.client('s3')
    # path = "http://" + bucket + ".s3.ap-northeast-2.amazonaws.com/" + fn
    # s3.upload_file('/tmp/'+fn, bucket, fn)

    return ret