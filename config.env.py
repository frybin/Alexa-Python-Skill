from os import environ as env

# Flask config
IP = env.get('IP', '0.0.0.0')
PORT = env.get('PORT', 8080)
SERVER_NAME = env.get('SERVER_NAME', 'rss-skill.csh.rit.edu')

# DB Info
SQLALCHEMY_DATABASE_URI = env.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = 'False'

#WTF Form Secret
SECRET_KEY = env.get('SECRET_KEY')
