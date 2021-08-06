#!/usr/bin/env python3
"""This application requests mods from the Steam workshop
and posts them to Discord webhooks."""
# TODO add args e.g. max_mods; add func to sub to game

import datetime
import hashlib
import json
import os
import re
import sys
import functools

import requests

from constants import *


def debug(func):
    """Print the function signature and return value"""
    if VERBOSE > 0:
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)

            print(f"Calling {func.__name__}({signature})\n")
            value = func(*args, **kwargs)
            print(f"{func.__name__!r} returned {value!r}\n")

            return value

        return wrapper_debug
    else:
        return func


@debug
def keyhash(string):
    """Hash the string using sha-1 and output a hex digest. Helpful for anonymizing known_mods."""
    return hashlib.sha1(string.encode('utf-8')).hexdigest()


@debug
def get_latest_mods(app_id):
    """Returns the latest 10 mods for the given consumer app id."""
    BUILT_QUERY_URL = "%s&format=%s&query_type=%i&page=%i&numperpage=%i&creator_appid=%i&appid=%s&filetype=%i" % (
        QUERY_URL, "json", 1, 1, MAX_MODS, 0, "%i", 0)
    query = BUILT_QUERY_URL % app_id
    print(query)
    try:
        req = requests.get(query)
        print(req)
        if req.status_code == 200:
            response = json.loads(req.text)
            mod_arr = response["response"]["publishedfiledetails"]
            return list(map(lambda x: int(x["publishedfileid"]), mod_arr))
    except requests.exceptions.RequestException as req_exc:
        print(req_exc)
        return []


@debug
def determine_mods_to_request(handled_mods):
    """Finds the mods that need to be posted to at least one channel."""
    app_ids = set()
    new_mods = set()

    if "SDWEBHOOK_MANUALLY_POST" in os.environ:
        return [int(os.environ["SDWEBHOOK_MANUALLY_POST"])]

    for hook in HOOKS:
        for app_id in hook["ids"]:
            app_ids.add(app_id)

    for app_id in app_ids:
        mods = get_latest_mods(app_id)
        for posted in handled_mods.values():
            list_of_posted = posted.get(str(app_id))
            if list_of_posted != None:
                if list_of_posted != []:
                    to_post_for = [
                        mod_id for mod_id in mods
                        if mod_id not in list_of_posted
                    ]
                    new_mods.update(to_post_for)
                else:
                    posted[str(app_id)] = mods

    return list(new_mods)


@debug
def get_game_name(handled_mods, app_id):
    if str(app_id) not in handled_mods:
        handled_mods[str(app_id)] = dict()

    if "game_name" in handled_mods[str(app_id)]:
        return handled_mods[str(app_id)]["game_name"]
    else:
        req = requests.get(APPDETAILS_URL % app_id)
        if req.status_code == 200:
            name = json.loads(req.text)[str(app_id)]["data"]["name"]
            handled_mods[str(app_id)]["game_name"] = name
            return name

    return None


@debug
def post_mod(handled_mods, mod, user):
    """Post the mod and add it to handled_mods if successful"""
    publishedfileid = int(mod["publishedfileid"])
    app_id = int(mod["consumer_app_id"])
    game_name = get_game_name(handled_mods, app_id)

    embed = {}
    wk_obj = {'embeds': [{}]}
    embed["title"] = "%s" % (mod["title"])
    embed["type"] = "rich"
    embed[
        "url"] = "http://steamcommunity.com/sharedfiles/filedetails/?id=%i" % (
        publishedfileid)
    embed["description"] = re.sub(r"\[.*?\]", '', mod["description"].replace(
        "\r\n", " "))[:200] + '\u2026'
    embed["color"] = 3447003
    embed["timestamp"] = datetime.datetime.utcfromtimestamp(
        mod["time_created"]).isoformat()

    embed["author"] = {}
    embed["author"]["name"] = user["personaname"]
    embed["author"]["url"] = user["profileurl"]
    embed["author"]["proxy_icon_url"] = user["profileurl"]
    embed["author"]["icon_url"] = user["avatar"]

    embed["thumbnail"] = {}
    embed["thumbnail"]["url"] = mod["preview_url"]
    embed["thumbnail"]["proxy_url"] = user["profileurl"]
    embed["thumbnail"]["height"] = 84
    embed["thumbnail"]["width"] = 84

    if game_name:
        embed["footer"] = {}
        embed["footer"]["text"] = "New %s mod release" % game_name

    wk_obj["embeds"][0] = embed
    headers = {'Content-type': 'application/json'}
    for hook in HOOKS:
        if app_id in hook["ids"]:
            hashed = keyhash(hook["url"])
            if publishedfileid not in handled_mods[hashed][str(app_id)]:
                if DRY_RUN:
                    handled_mods[hashed][str(app_id)].append(publishedfileid)
                else:
                    try:
                        req = requests.post(hook["url"],
                                            data=json.dumps(wk_obj),
                                            headers=headers)
                        if req.status_code == 204:
                            handled_mods[hashed][str(app_id)].append(publishedfileid)
                    except requests.exceptions.RequestException as req_exc:
                        print(req_exc)


@debug
def get_users(users_list):
    """Retrieve all users' profiles"""
    formatted_list = ",".join(users_list)
    built_get = "%s&steamids=%s" % (GETPLAYERSUMM_URL, formatted_list)
    try:
        req = requests.get(built_get)
        if req.status_code == 200:
            response = json.loads(req.text)["response"]["players"]
            players = {}
            for player in response:
                players[player["steamid"]] = player
            return players
    except requests.exceptions.RequestException as req_exc:
        print(req_exc)

    return []


@debug
def post_new_mods(handled_mods):
    """Determine the mods to request, request them, and pst to the correct channels"""
    mod_ids = determine_mods_to_request(handled_mods)
    print(mod_ids)
    if len(mod_ids) > 0:
        data = {'key': WEBKEY, 'itemcount': len(mod_ids)}
        for idx, i in enumerate(mod_ids):
            print(i)
            data["publishedfileids[%i]" % idx] = i
        try:
            i = requests.post(POST_URL, data=data)
            if i.status_code == 200:
                response = json.loads(i.text)["response"]
                if response["result"] == 1:
                    sorted_mods = sorted(response["publishedfiledetails"],
                                         key=lambda f: f["time_created"])
                    users = get_users(map(lambda x: x["creator"], sorted_mods))
                    for mod in sorted_mods:
                        print(mod)
                        post_mod(handled_mods, mod, users[mod["creator"]])
        except requests.exceptions.RequestException as req_exc:
            print(req_exc)


def main():
    try:
        with open('known_mods', 'a+') as k_m_file:
            try:
                k_m_file.seek(0)
                known_mods = dict(toml.load(k_m_file))
            except Exception:
                known_mods = dict()

            for hook in HOOKS:
                hashed = keyhash(hook["url"])
                if not hashed in known_mods:
                    posted = dict()
                    for app_id in hook["ids"]:
                        posted[str(app_id)] = list()
                    known_mods[hashed] = posted
    except EnvironmentError as err:
        print(err)
        sys.exit(1)

    print(known_mods)
    post_new_mods(known_mods)

    # Cleanup -- if we request the latest 10 mods, keep the latest 20 posted.
    # This gives some slack space in case users delete or unlist mods.
    for key, val in known_mods.items():
        if len(key) == 40:  # SHA-1 hash
            for app_id in val.keys():
                val[app_id] = sorted(val[app_id])[-(MAX_MODS * 2):]

    try:
        with open('known_mods', 'w+') as k_m_file:
            toml.dump(known_mods, k_m_file)
    except EnvironmentError as err:
        print(err)
        sys.exit(1)

    print("[%s] Success!" % (datetime.datetime.now().isoformat()))
    sys.exit(0)


def pmb_hook():
    main()

if __name__ == "__main__":
    main()

