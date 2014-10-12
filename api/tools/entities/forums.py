__author__ = 'dmitry'

from api.tools import DBconnect
from api.tools.entities import users


def save_forum(name, short_name, user):
    DBconnect.exist(entity="user", identifier="email", value=user)
    forum = DBconnect.select_query(
        'select id, name, short_name, user FROM forum WHERE short_name = %s', (short_name, )
    )
    if len(forum) == 0:
        DBconnect.update_query('INSERT INTO forum (name, short_name, user) VALUES (%s, %s, %s)',
                               (name, short_name, user, ))
        forum = DBconnect.select_query(
            'select id, name, short_name, user FROM forum WHERE short_name = %s', (short_name, )
        )
    return forum_description(forum)


def forum_description(forum):
    forum = forum[0]
    response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }
    return response


def details(short_name, related):
    forum = DBconnect.select_query(
        'select id, name, short_name, user FROM forum WHERE short_name = %s', (short_name, )
    )
    if len(forum) == 0:
        raise ("No forum with exists short_name=" + short_name)
    forum = forum_description(forum)

    if "user" in related:
        forum["user"] = users.details(forum["user"])
    return forum


def list_users(short_name, optional):
    DBconnect.exist(entity="forum", identifier="short_name", value=short_name)

    query = "SELECT distinct email FROM user JOIN post ON post.user = user.email " \
            " JOIN forum on forum.short_name = post.forum WHERE post.forum = %s "
    if "since_id" in optional:
        query += " AND user.id >= " + str(optional["since_id"])
    if "order" in optional:
        query += " ORDER BY user.id " + optional["order"]
    if "limit" in optional:
        query += " LIMIT " + str(optional["limit"])

    users_tuple = DBconnect.select_query(query, (short_name, ))
    list_u = []
    for user in users_tuple:
        user = user[0]
        list_u.append(users.details(user))
    return list_u
