import toml


# Set to true to not post. Useful for migrating from an earlier version of the
# script without posting
DRY_RUN = False

MAX_MODS = 10

CONFIG = toml.load(open('../../Data/config.toml'))

WEBKEY = CONFIG["config"]["webkey"]

HOOKS = CONFIG["hook"]

QUERY_URL = "https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/?key=%s" % (
    WEBKEY)

GETPLAYERSUMM_URL = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=%s" % (
    WEBKEY)

POST_URL = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"


APPDETAILS_URL = "https://store.steampowered.com/api/appdetails?key=%s&appids=%s" % (WEBKEY, "%i")

VERBOSE = 1
