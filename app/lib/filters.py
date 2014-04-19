import datetime
import re

from dojang.escape import simple_escape, html_escape
from lib.bbcode import *
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from tornado import escape
import tornado.locale
from tornado.options import options


__all__ = ['markup', 'markdown', 'xmldatetime']


_emoji_list = [
    "-1", "0", "1", "109", "2", "3", "4", "5", "6", "7", "8", "8ball", "9",
    "a", "ab", "airplane", "alien", "ambulance", "angel", "anger", "angry",
    "apple", "aquarius", "aries", "arrow_backward", "arrow_down",
    "arrow_forward", "arrow_left", "arrow_lower_left", "arrow_lower_right",
    "arrow_right", "arrow_up", "arrow_upper_left", "arrow_upper_right",
    "art", "astonished", "atm", "b", "baby", "baby_chick", "baby_symbol",
    "balloon", "bamboo", "bank", "barber", "baseball", "basketball", "bath",
    "bear", "beer", "beers", "beginner", "bell", "bento", "bike", "bikini",
    "bird", "birthday", "black_square", "blue_car", "blue_heart", "blush",
    "boar", "boat", "bomb", "book", "boot", "bouquet", "bow", "bowtie",
    "boy", "bread", "briefcase", "broken_heart", "bug", "bulb",
    "bullettrain_front", "bullettrain_side", "bus", "busstop", "cactus",
    "cake", "calling", "camel", "camera", "cancer", "capricorn", "car",
    "cat", "cd", "chart", "checkered_flag", "cherry_blossom", "chicken",
    "christmas_tree", "church", "cinema", "city_sunrise", "city_sunset",
    "clap", "clapper", "clock1", "clock10", "clock11", "clock12", "clock2",
    "clock3", "clock4", "clock5", "clock6", "clock7", "clock8", "clock9",
    "closed_umbrella", "cloud", "clubs", "cn", "cocktail", "coffee",
    "cold_sweat", "computer", "confounded", "congratulations",
    "construction", "construction_worker", "convenience_store", "cool",
    "cop", "copyright", "couple", "couple_with_heart", "couplekiss", "cow",
    "crossed_flags", "crown", "cry", "cupid", "currency_exchange", "curry",
    "cyclone", "dancer", "dancers", "dango", "dart", "dash", "de",
    "department_store", "diamonds", "disappointed", "dog", "dolls",
    "dolphin", "dress", "dvd", "ear", "ear_of_rice", "egg", "eggplant",
    "egplant", "eight_pointed_black_star", "eight_spoked_asterisk",
    "elephant", "email", "es", "european_castle", "exclamation", "eyes",
    "factory", "fallen_leaf", "fast_forward", "fax", "fearful", "feelsgood",
    "feet", "ferris_wheel", "finnadie", "fire", "fire_engine", "fireworks",
    "fish", "fist", "flags", "flushed", "football", "fork_and_knife",
    "fountain", "four_leaf_clover", "fr", "fries", "frog", "fuelpump", "gb",
    "gem", "gemini", "ghost", "gift", "gift_heart", "girl", "goberserk",
    "godmode", "golf", "green_heart", "grey_exclamation", "grey_question",
    "grin", "guardsman", "guitar", "gun", "haircut", "hamburger", "hammer",
    "hamster", "hand", "handbag", "hankey", "hash", "headphones", "heart",
    "heart_decoration", "heart_eyes", "heartbeat", "heartpulse", "hearts",
    "hibiscus", "high_heel", "horse", "hospital", "hotel", "hotsprings",
    "house", "hurtrealbad", "icecream", "id", "ideograph_advantage", "imp",
    "information_desk_person", "iphone", "it", "jack_o_lantern",
    "japanese_castle", "joy", "jp", "key", "kimono", "kiss", "kissing_face",
    "kissing_heart", "koala", "koko", "kr", "leaves", "leo", "libra", "lips",
    "lipstick", "lock", "loop", "loudspeaker", "love_hotel", "mag",
    "mahjong", "mailbox", "man", "man_with_gua_pi_mao", "man_with_turban",
    "maple_leaf", "mask", "massage", "mega", "memo", "mens", "metal",
    "metro", "microphone", "minidisc", "mobile_phone_off", "moneybag",
    "monkey", "monkey_face", "moon", "mortar_board", "mount_fuji", "mouse",
    "movie_camera", "muscle", "musical_note", "nail_care", "necktie", "new",
    "no_good", "no_smoking", "nose", "notes", "o", "o2", "ocean", "octocat",
    "octopus", "oden", "office", "ok", "ok_hand", "ok_woman", "older_man",
    "older_woman", "open_hands", "ophiuchus", "palm_tree", "parking",
    "part_alternation_mark", "pencil", "penguin", "pensive", "persevere",
    "person_with_blond_hair", "phone", "pig", "pill", "pisces", "plus1",
    "point_down", "point_left", "point_right", "point_up", "point_up_2",
    "police_car", "poop", "post_office", "postbox", "pray", "princess",
    "punch", "purple_heart", "question", "rabbit", "racehorse", "radio",
    "rage", "rage1", "rage2", "rage3", "rage4", "rainbow", "raised_hands",
    "ramen", "red_car", "red_circle", "registered", "relaxed", "relieved",
    "restroom", "rewind", "ribbon", "rice", "rice_ball", "rice_cracker",
    "rice_scene", "ring", "rocket", "roller_coaster", "rose", "ru", "runner",
    "sa", "sagittarius", "sailboat", "sake", "sandal", "santa", "satellite",
    "satisfied", "saxophone", "school", "school_satchel", "scissors",
    "scorpius", "scream", "seat", "secret", "shaved_ice", "sheep", "shell",
    "ship", "shipit", "shirt", "shit", "shoe", "signal_strength",
    "six_pointed_star", "ski", "skull", "sleepy", "slot_machine", "smile",
    "smiley", "smirk", "smoking", "snake", "snowman", "sob", "soccer",
    "space_invader", "spades", "spaghetti", "sparkler", "sparkles",
    "speaker", "speedboat", "squirrel", "star", "star2", "stars", "station",
    "statue_of_liberty", "stew", "strawberry", "sunflower", "sunny",
    "sunrise", "sunrise_over_mountains", "surfer", "sushi", "suspect",
    "sweat", "sweat_drops", "swimmer", "syringe", "tada", "tangerine",
    "taurus", "taxi", "tea", "telephone", "tennis", "tent", "thumbsdown",
    "thumbsup", "ticket", "tiger", "tm", "toilet", "tokyo_tower", "tomato",
    "tongue", "top", "tophat", "traffic_light", "train", "trident",
    "trollface", "trophy", "tropical_fish", "truck", "trumpet", "tshirt",
    "tulip", "tv", "u5272", "u55b6", "u6307", "u6708", "u6709", "u6e80",
    "u7121", "u7533", "u7a7a", "umbrella", "unamused", "underage", "unlock",
    "up", "us", "v", "vhs", "vibration_mode", "virgo", "vs", "walking",
    "warning", "watermelon", "wave", "wc", "wedding", "whale", "wheelchair",
    "white_square", "wind_chime", "wink", "wink2", "wolf", "woman",
    "womans_hat", "womens", "x", "yellow_heart", "zap", "zzz", "+1"
]


def _emoji(text):
    if not hasattr(options, 'emoji_url'):
        return text

    if not options.emoji_url:
        return text

    pattern = re.compile(':([a-z0-9\+\-_]+):')

    def make_emoji(m):
        name = m.group(1)
        if name not in _emoji_list:
            return ':%s:' % name
        tpl = ('<img class="emoji" title="%(name)s" alt="%(name)s" height="20"'
               ' width="20" src="%(url)s%(name)s.png" align="top">')
        return tpl % {'name': name, 'url': options.emoji_url}

    text = pattern.sub(make_emoji, text)
    return text




# get link back
def makelink(m):
    link = m.group(1)
    print "makelink", link
    title = link #.replace('http://', '').replace('https://', '')
    # if len(title) > 40:
    #     title = title[:40] + '...'
    if link.startswith('http://') or link.startswith('https://'):
        return '<a href="%s" rel="nofollow" class="link" target="_blank">%s</a>' % (link, title)
    return '<a href="http://%s" rel="nofollow" class="link" target="_blank">%s</a>' % (link, title)

def bbcode_link(m):
    link = m.group(1)
    return '[url]%s[/url]' % (link)

    # print "makelink", link
    # title = link #.replace('http://', '').replace('https://', '')
    # # if len(title) > 40:
    # #     title = title[:40] + '...'
    # if link.startswith('http://') or link.startswith('https://'):
    #     return '<a href="%s" rel="nofollow" class="link" target="_blank">%s</a>' % (link, title)
    # return '<a href="http://%s" rel="nofollow" class="link" target="_blank">%s</a>' % (link, title)

def autolink(text):
    # http://daringfireball.net/2010/07/improved_regex_for_matching_urls
    pattern = re.compile(
        r'(?m)((?:http?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}'
        r'/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+'
        r'|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>???]))')
    text = pattern.sub(bbcode_link, text)
    pattern = re.compile(
        r'(?i)(?:&lt;)((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}'
        r'/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+'
        r'|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>???]))(?:&gt;)')
    text = pattern.sub(bbcode_link, text)
    return text


def youku(value):
    if value is None:
        return None
    videos = re.findall('(http://v.youku.com/v_show/id_[a-zA-Z0-9\=]+.html)\s?', value)
    if (len(videos) > 0):
        for video in videos:
            video_id = re.findall('http://v.youku.com/v_show/id_([a-zA-Z0-9\=]+).html', video)
            value = value.replace('http://v.youku.com/v_show/id_' + video_id[0] + '.html',
                                  '<embed src="http://player.youku.com/player.php/sid/' + video_id[0] + '/v.swf" allowFullScreen="true" quality="high" width="480" height="400" align="middle" allowScriptAccess="always" type="application/x-shockwave-flash"></embed>')
        return value
    else:
        return value

def sinaimglink(m):
    link = m.group(1)    
    return '[img]%s[/img]' % (link)

def sinaimg(value):
    if value is None:
        return None
    pattern = re.compile('(http://[a-z0-9]+.sinaimg.cn/[a-zA-Z0-9]+/[a-zA-Z0-9]+.[jpg|png|gif]+)\s?')
    return pattern.sub(sinaimglink, value)


#def br_escape(html):
#    if html is None:
#        return None;
#    html = re.sub('[\r\n]+', ' <p></p> ', html)
#    return html



def make_mention(m):
    name = m.group(1)
    return '[url=%s/people/u/%s]@[b]%s[/b][/url] '%(options.site_url, name, name)
    # return ' <b><a href="/people/u/%s" class="username">@%s</a></b> ' % (name, name)

def automention(text):
    if text is None:
        return None
    pattern = re.compile(r'@([a-zA-Z0-9\-\_\u4e00-\u9fa5]+)')
    text = pattern.sub(make_mention, text)
    return text

def markup(text):
    if text is None:
        return ""
    return render_bbcode(automention(sinaimg((text))))



