import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

db = SQLAlchemy(app)

# pylint: disable=wrong-import-position
from rss_skill.models import Feed
from .utils import feed_parser

test = Feed.query.all()
for feed in test:
    info, hashed = feed_parser(feed.link, feed.article_1, feed.article_2)
    print(info)
    print(hashed)
    