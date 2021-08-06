#!/usr/bin/python3

from os import path, getenv

from dotenv import load_dotenv
from googletrans.constants import LANGCODES

##################
# File Locations #
##################
DEFAULT_DIR = path.dirname(path.abspath(__file__))
PUBLIC_DIR = path.join(DEFAULT_DIR, '/docs/')

##################
# Bot & API Info #
##################
load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
POC_TOKEN = getenv('POC_TOKEN')
GUILD = getenv('DISCORD_GUILD')
WOLFRAM = getenv('WOLFRAM_TOKEN')
STEAM_TOKEN = getenv('STEAM_TOKEN')
SPIDER2 = getenv('SPIDER2')
VERSION = '08.05.2021'
LICENSE = "AGPL-3.0"
LICENSE_URL = "https://opensource.org/licenses/AGPL-3.0"
LICENSE_FILE = path.join(DEFAULT_DIR, 'LICENSE')
ABOUT = 'Python port of Muffalo  BOT'
ABOUT_URL = 'https://github.com/EanNewton/MuffaloBot'
ABOUT_FILE = 'about.txt'
VERBOSE = 1

#################################
# Internal Function Static Data #
#################################
# combine all 2 letter codes and fully qualified names into flat list from a dict()
LANGCODES = [each for tuple_ in LANGCODES.items() for each in tuple_]
ID_CODES = {
    'rimworld': 294100,
}

DIVIDER = '<<>><<>><<>><<>><<>><<>><<>><<>><<>>\n'
QUOTES_URL = 'https://raw.githubusercontent.com/spdskatr/MuffaloBot/master/MuffaloBot/Data/data.json'
QUOTES_BASE = {
    "!moddingtutorials": "http://rimworldwiki.com/wiki/Modding_Tutorials",
    "!settingupcs": "http://rimworldwiki.com/wiki/Modding_Tutorials/Setting_up_a_solution",
    "!patchoperations": "http://rimworldwiki.com/wiki/Modding_Tutorials/PatchOperations",
    "!ignis": "https://cdn.discordapp.com/attachments/225701528470683648/387460314918289408/unknown-4.png",
    "!killignis": "https://cdn.discordapp.com/attachments/225701528470683648/387458918973964288/dont.png",
    "!radish": "http://prntscr.com/hj6kji",
    "!moddingresources": "https://spdskatr.github.io/RWModdingResources/",
    "!op": "<:op:431028261032558603>",
    "!OP": "https://cdn.discordapp.com/emojis/431028261032558603.png?v=1",
    "!stan": "`!stan` is not a command. Please try again lat- oh wait. It is.",
    "!platter": "\"You had your solution handed to you on a silver platter, why do you reject it?\" - Mehni",
    "!havefun": "\"well, have fun with that then\" - erdelf",
    "!battleroyale": "https://imgur.com/9c622iQ",
    "!transpiling": "\"Transpiling is like playing with your very own quantum teleportation device. Don't fuck up and you can do great things\" - Spdskatr",
    "!conbat": "https://cdn.discordapp.com/attachments/214523406727512065/464757203723616258/unknown.png",
    "!extamded": "https://cdn.discordapp.com/attachments/235909071805349888/323085458433114113/Conbat.png",
    "!quantum": "\"If you think you understand quantum mechanics, you don't understand quantum mechanics.\" - Richard Feynman",
    "!seriousbusiness": "\"I'm seriously business mod\" - Mehni",
    "!troublepins": "In #troubleshooting, be sure to read the pinned messages or follow this link: https://discordapp.com/channels/214523379766525963/257987178834034688/648015871910084608",
    "!incompatible": "https://media.discordapp.net/attachments/632790371256238120/671190029217038366/CEIAMINCOMPAT.png",
    "!modideas": "Friendly reminder to search for mods in <#218913447788806144> before coming to <#224106027413405696> to suggest them :)",
    "!hellomodder": "Hello modder. I am here to inform you that all mods need to update Harmony and should make Harmony a dependent mod. Also include CE compatibility. RimWorld 1.1 is out. Thanks.",
    "!jdaltpantysearch": "don't",
    "!ce": "https://cdn.discordapp.com/attachments/224106027413405696/723660787775963197/CEDRAKEMEME.png",
    "!modabuse": "https://cdn.discordapp.com/attachments/225701528470683648/728164594585042984/modabuse.png",
    "!csharpis": "\"C# is a matter of effort, not possibility\" - Jdalt40"
}
EXTSET = {
    'image': [
        'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'
    ],
    'audio': [
        '3gp', 'aa', 'aac', 'aax', 'act', 'aiff', 'alac', 'amr',
        'ape', 'au', 'awb', 'dct', 'dss', 'dvf', 'flac', 'gsm',
        'iklax', 'ivs', 'm4a', 'm4b', 'm4p', 'mmf', 'mp3', 'mpc',
        'msv', 'nmf', 'nsf', 'ogg', 'oga', 'mogg', 'opus', 'ra',
        'rm', 'raw', 'rf64', 'sln', 'tta', 'voc', 'vox', 'wav',
        'wma', 'wv', 'webm', '8svx', 'cda'
    ],
    'video': [
        'webm', 'mkv', 'flv', 'vob', 'ogv', 'ogg', 'drc',
        'gifv', 'mng', 'avi', 'mts', 'm2ts', 'ts', 'mov', 'qt',
        'wmv', 'yuv', 'rm', 'rmvb', 'asf', 'amv', 'mp4', 'm4p',
        'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'm4v', 'svi',
        '3gp', '3g2', 'mxf', 'roq', 'nsv', 'f4v', 'f4p', 'f4a', 'f4b'
    ],
    'document': [
        '0', '1st', '600', '602', 'abw', 'acl', 'afp', 'ami',
        'ans', 'ascaww', 'ccf', 'csv', 'cwk', 'dbk', 'dita', 'doc',
        'docm', 'docx', 'dotdotx', 'dwd', 'egt', 'epub', 'ezw',
        'fdx', 'ftm', 'ftx', 'gdoc', 'html', 'hwp', 'hwpml', 'log',
        'lwp', 'mbp', 'md', 'me', 'mcw', 'mobinb', 'nbp', 'neis',
        'odm', 'odoc', 'odt', 'osheet', 'ott', 'ommpages', 'pap',
        'pdax', 'pdf', 'quox', 'rtf', 'rpt', 'sdw', 'sestw',
        'sxw', 'tex', 'info', 'troff', 'txt', 'uof', 'uoml', 'viawpd',
        'wps', 'wpt', 'wrd', 'wrf', 'wri', 'xhtml', 'xht', 'xml', 'xps'
    ]
}
