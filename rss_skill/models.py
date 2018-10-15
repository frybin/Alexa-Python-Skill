####################################
# File name: models.py             #
# Author: Fred Rybin               #
####################################
from rss_skill import db

class Feed(db.Model):
    __tablename__ = 'feed'

    rss_i = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
    article_1 = db.Column(db.Text, nullable=False)
    article_2 = db.Column(db.Text, nullable=False)
    post = db.Column(db.String(32), nullable=False)

    def __init__(self, name, link, article_1, article_2):
        self.name = name
        self.link = link
        self.article_1 = article_1
        self.article_2 = article_2
        self.post = ""

    def __repr__(self):
        return f'Feed {self.rss_i}: {self.name}'
