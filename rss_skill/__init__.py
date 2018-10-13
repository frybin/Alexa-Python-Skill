import os
from flask import Flask, render_template
from flask_ask import Ask, statement, question
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
import rss_skill.routes
from .utils import feed_parser

@ask.intent('AllRSSWordIntent')
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
    if feed_info:
        response = ", ".join(feed_info)
    else:
        response = "There were no data found"
    return response

@ask.launch
def launch():
    response = "Would you like to hear your updates or your feeds?"
    return question(response).simple_card('', response)

@ask.intent('RSSLinkIntent')
def get_all_feeds():
    feeds = Feed.query.all()
    feed_info = ["Would you like to hear the feeds for: "]
    i = 1
    for feed in feeds:
        feed_info.append(f"{feed.rss_i}, {feed.name}")
        if i < len(feeds):
            feed_info.append("or")
        i = i+1
    if feed_info:
        response = " ".join(feed_info)
    else:
        response = "There were no data found"
    return question(response).simple_card('', response)

@ask.intent('RSSWordIntent', mapping={'rss_id': 'feedname'})
def get_info_single_feed(rss_id):
    feed = Feed.query.get(rss_id)
    feed_info = []
    info, hashed = feed_parser(feed.link, feed.article_1, feed.article_2)
    feed.post = hashed
    db.session.commit()
    for data in info:
        feed_info.extend(data[:-1])
    if feed_info:
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
    if feed_info:
        response = ", ".join(feed_info)
    else:
        response = "There were no updates found"
    return statement(response).simple_card('', response)

@ask.intent('AMAZON.HelpIntent')
def help_intent():
    response = ("This is a RSS Feed Reader Skill, To hear your updates"
               " say updates or to hear a specific feed please say feeds")
    return question(response).simple_card('', response)

@ask.intent('AMAZON.CancelIntent')
def cancel_intent():
    response = "Thank you for using the RSS Reader, Goodbye"
    return statement(response).simple_card('', response)

@ask.intent('AMAZON.StopIntent')
def stop_intent():
    response = "Thank you for using the RSS Reader, Goodbye"
    return statement(response).simple_card('', response)

@ask.session_ended
def session_ended():
    return "{}", 200
