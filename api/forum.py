from api.tools.entities import forums, posts, threads
from flask import Blueprint, request
from api.helpers import related_exists, choose_required, intersection, get_json
import json
import common
from tools import DBconnect
import MySQLdb

module = Blueprint('forum', __name__, url_prefix='/db/api/forum')


@module.route("/create/", methods=["POST"])
def create():
    content = request.json
    required_data = ["name", "short_name", "user"]
    try:
        choose_required(data=content, required=required_data)
        forum = forums.save_forum(name=content["name"], short_name=content["short_name"],
                                  user=content["user"])
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": forum})


@module.route("/details/", methods=["GET"])
def details():
    get_params = get_json(request)
    required_data = ["forum"]
    related = related_exists(get_params)
    try:
        choose_required(data=get_params, required=required_data)
        forum = forums.details(short_name=get_params["forum"], related=related)
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": forum})


@module.route("/listThreads/", methods=["GET"])
def list_threads():
    content = get_json(request)
    required_data = ["forum"]
    related = related_exists(content)
    optional = intersection(request=content, values=["limit", "order", "since"])
    try:
        choose_required(data=content, required=required_data)
        threads_l = threads.thread_list(entity="forum", identifier=content["forum"],
                                         related=related, params=optional)
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": threads_l})


@module.route("/listPosts/", methods=["GET"])
def list_posts():
    # content = get_json(request)
    # required_data = ["forum"]
    # related = related_exists(content)
    #
    # optional = intersection(request=content, values=["limit", "order", "since"])
    # # try:
    # choose_required(data=content, required=required_data)
    # posts_l = posts.posts_list(entity="forum", params=optional, identifier=content["forum"],
    #                                related=related)

    forum = request.args.get('forum', None)
    since = request.args.get('since', '0000-00-00 00:00:00')
    limit = request.args.get('limit', 18446744073709551615)  # TODO: hard code
    order = request.args.get('order', 'desc')
    related = request.args.getlist('related')

    limit = long(limit)  # TODO: bad code

    cursor = DBconnect.connect().cursor(MySQLdb.cursors.DictCursor)
    if order == 'desc':
        cursor.execute("""SELECT * FROM `posts` WHERE `forum` = %s AND `date` >= %s ORDER BY `date` DESC LIMIT %s;""",
                       (forum, since, limit))  # TODO: bad code - excess condition
    else:
        cursor.execute("""SELECT * FROM `posts` WHERE `forum` = %s AND `date` >= %s ORDER BY `date` ASC LIMIT %s;""",
                       (forum, since, limit))  # TODO: bad code - excess condition

    posts = [i for i in cursor.fetchall()]

    for post in posts:
        if 'user' in related:
            user = common.user_details(cursor, post['user'])
            post.update({'user': user})

        if 'forum' in related:
            forum = common.forum_details(cursor, post['forum'])
            post.update({'forum': forum})

        if 'thread' in related:
            thread = common.thread_details(cursor, post['thread'])
            post.update({'thread': thread})

        post.update({'date': str(post['date'])})  # TODO: bad code

    cursor.close()

    # except Exception as e:
    #     return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": posts})


@module.route("/listUsers/", methods=["GET"])
def list_users():
    content = get_json(request)
    required_data = ["forum"]
    optional = intersection(request=content, values=["limit", "order", "since_id"])
    # try:
    choose_required(data=content, required=required_data)
    users_l = forums.list_users(content["forum"], optional)
    # except Exception as e:
    #     return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": users_l})
