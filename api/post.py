from api.tools.entities import posts
from flask import Blueprint, request
import json
from api.helpers import choose_required, intersection, related_exists, get_json


module = Blueprint('post', __name__, url_prefix='/post')


@module.route("/create/", methods=["POST"])
def create():
    content = request.json
    required_data = ["user", "forum", "thread", "message", "date"]
    optional_data = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
    optional = intersection(request=content, values=optional_data)
    try:
        choose_required(data=content, required=required_data)
        post = posts.create(date=content["date"], thread=content["thread"],
                            message=content["message"], user=content["user"],
                            forum=content["forum"], optional=optional)
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": post})


@module.route("/details/", methods=["GET"])
def details():
    content = get_json(request)
    required_data = ["post"]
    related = related_exists(content)
    try:
        choose_required(data=content, required=required_data)
        post = posts.details(content["post"], related=related)
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": post})


def post_list(request):
    content = request.GET.dict()
    try:
        identifier = content["forum"]
        entity = "forum"
    except KeyError:
        try:
            identifier = content["thread"]
            entity = "thread"
        except Exception as e:
            return json.dumps({"code": 1, "response": (e.message)})

    optional = intersection(request=content, values=["limit", "order", "since"])
    try:
        p_list = posts.posts_list(entity=entity, params=optional, identifier=identifier, related=[])
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": p_list})


def remove(request):
    content = json.loads(request.body)
    required_data = ["post"]
    try:
        choose_required(data=content, required=required_data)
        post = posts.remove_restore(post_id=content["post"], status=1)
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": post})


def restore(request):
    content = json.loads(request.body)
    required_data = ["post"]
    try:
        choose_required(data=content, required=required_data)
        post = posts.remove_restore(post_id=content["post"], status=0)
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": post})


def update(request):
    content = json.loads(request.body)
    required_data = ["post", "message"]
    try:
        choose_required(data=content, required=required_data)
        post = posts.update(update_id=content["post"], message=content["message"])
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": post})


def vote(request):
    content = json.loads(request.body)
    required_data = ["post", "vote"]
    try:
        choose_required(data=content, required=required_data)
        post = posts.vote(vote_id=content["post"], vote_type=content["vote"])
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": post})
