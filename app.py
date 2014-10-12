__author__ = 'dmitry'

from flask import Flask

app = Flask(__name__)

app.config['DEBUG'] = True

from api.thread import module as thread
from api.user import module as user
from api.forum import module as forum
from api.post import module as post
# from api.admin import mod as admin_api

app.register_blueprint(user)
app.register_blueprint(forum)
app.register_blueprint(thread)
app.register_blueprint(post)
# app.register_blueprint(admin_api)


if __name__ == '__main__':
    app.run(port=8080)
