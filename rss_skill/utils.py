import hashlib
import pickle
import feedparser

def hash_object(data):
    data_pickle = pickle.dumps(data)
    result = hashlib.md5(data_pickle).hexdigest()
    return result

def feed_parser(link, tag1='title', tag2='summary'):
    data = []
    feed = feedparser.parse(link)
    hashed = 0
    for post in feed.entries:
        simple = [post[tag1]]
        if hashed == 0:
            hashed = hash_object(post)
        try:
            simple.append(post[tag2])
        except:
            pass
        data.append(simple)
    return data, hashed

if __name__ == "__main__":
    feed_parser('https://mycourses.rit.edu/d2l/le/news/rss/713138/course?token=avafqi245o0qvo7ddd22&ou=713138')
