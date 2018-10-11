import os
from flask import Flask
from flask_ask import Ask, statement
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
ask = Ask(app, '/')

# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

db = SQLAlchemy(app)

# pylint: disable=wrong-import-position
from rss_skill.models import Feed
from .utils import feed_parser

def get_all_info_feeds():
    feeds = Feed.query.all()
    feed_info = []
    for feed in feeds:
        info, hashed = feed_parser(feed.link, feed.article_1, feed.article_2)
        feed.post = hashed
        db.session.commit()
        feed_info.append(f"Updates for {feed.name}")
        for data in info:
            feed_info.extend(data[:-1])
    if len(feed_info) > 0:
        response = ", ".join(feed_info)
    else:
        response = "There were no data found"
    return response

@ask.intent('RSSWordIntent', mapping={'rss_id': 'feedname'})
def get_info_single_feed(rss_id):
    feed = Feed.query.get(rss_id)
    feed_info = []
    info, hashed = feed_parser(feed.link, feed.article_1, feed.article_2)
    feed.post = hashed
    db.session.commit()
    for data in info:
        feed_info.extend(data[:-1])
    if len(feed_info) > 0:
        response = ", ".join(feed_info)
    else:
        response = "There were no data found"
    return statement(response).simple_card('', response)

@ask.intent('UpdateFeedIntent')
def get_current_updates():
    feeds = Feed.query.all()
    feed_info = []
    for feed in feeds:
        info, hashed = feed_parser(feed.link, feed.article_1, feed.article_2)
        if hashed != feed.post:
            for data in info:
                if feed.post == data[len(data)-1]:
                    break
                feed_info.extend(data[:-1])
            feed.post = hashed
            db.session.commit()
    if len(feed_info) > 0:
        response = ", ".join(feed_info)
    else:
        response = "There were no updates found"
    return statement(response).simple_card('', response)

@ask.intent('RSSLinkIntent')
def get_all_feeds():
    feeds = Feed.query.all()
    feed_info = []
    for feed in feeds:
        feed_info.append(str(feed))
    if len(feed_info) > 0:
        response = ", ".join(feed_info)
    else:
        response = "There were no feeds found"
    return statement(response).simple_card('', response)

@ask.session_ended
def session_ended():
    return "{}", 200
