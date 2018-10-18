import hashlib
import pickle
import feedparser
import html2text
from bs4 import BeautifulSoup

def hash_object(data):
    data_pickle = pickle.dumps(data)
    result = hashlib.md5(data_pickle).hexdigest()
    return result

def feed_parser(link, tag1='title', tag2='summary'):
    h = html2text.HTML2Text()
    h.ignore_links = True
    data = []
    feed = feedparser.parse(link)
    hashed = 0
    for post in feed.entries:
        #simple = [h.handle(post[tag1])]
        simple = [''.join(BeautifulSoup(post[tag1]).findAll(text=True))]
        if hashed == 0:
            hashed = hash_object(post)
        try:
            #simple.append(h.handle(post[tag2]))
            simple.append(''.join(BeautifulSoup(post[tag2]).findAll(text=True)))
        except:
            pass
        simple.append(hash_object(post))
        data.append(simple)
    return data, hashed

if __name__ == "__main__":
    print(feed_parser(''))
