import datetime
import ipaddress
import json
import logging
import re
import socket
import struct
from collections import defaultdict
from html.parser import HTMLParser
from pprint import pformat, pprint

import mysql.connector
import requests
import sshtunnel
from bs4 import BeautifulSoup as bs

from TNT.func import stringify

LOGGER = logging.getLogger(__file__)

SITE_URL = "http://forum.tntvillage.scambioetico.org"

RESIDUALS = []
HAVE_RESIDUAL = None
DONE_POST = []

class MyHTMLParser(HTMLParser):

    def __init__(self, config=None):
        HTMLParser.__init__(self)
        self.els = []
        self.span = []

    def handle_starttag(self, tag, attrs):
        # print("%*sEncountered a start tag:" % (len(self.span)*2,"."),tag,pformat(attrs),pformat(self.span))
        if tag == "span":
            self.span.append(self.getpos())
        dattrs = dict(attrs)
        dattrs['0'] = 0
        self.attrs[tag].append(dattrs)
        args = ""
        if len(attrs) > 0:
            args = ' ' + ' '.join(["{}='{}'".format(k, v) for k, v in dict(attrs).items()])
        self.data.append('<{}{}{}>'.format(tag, "" if tag !=
                                           "span" else len(self.attrs[tag]), args))

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        # print("%*sEncountered a end tag:" % ( 2*len(self.span),"."), tag, pformat(self.span))
        if tag == "span":
            pos = self.span.pop()
            self.els.append(((pos, self.getpos())))
            # self.data.append('<Xspan %s,%s >' % (pos,self.getpos()))
        n = "" if tag != "span" else len(self.attrs[tag])
        if len(self.attrs[tag]) > 0:
            self.attrs[tag].pop()
        self.data.append('</{}{}>'.format(tag, n))

    def handle_data(self, data):
        self.data.append(data)

    def handle_comment(self, data):
        self.data.append("<!--{}-->".format(data))

    def feed(self, data):
        self.data = []
        self.attrs = defaultdict(list)
        HTMLParser.feed(self, data)
        return ''.join(self.data)

    def handle_entityref(self, name):
        self.data.append('&{};'.format(name))

    def handle_charref(self, name):
        self.data.append('&#{};'.format(name))


def todatestr(customTimestamp):
    date = datetime.datetime.fromtimestamp(customTimestamp)
    return date.strftime('%Y-%m-%d %H:%M:%S')


def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]


def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


def URLcheck(url):
    LOGGER.debug("URL Checking {}".format(url))
    try:
        request = requests.get(url)
        if request.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False


URL_MATCHES = (
    (r'^https?://forum.tntvillage.scambioetico.org/?showtopic=(\d+)', SITE_URL + 'viewtopic.php?t=\\1'),
    (r'^./?showtopic=(\d+)', SITE_URL + 'viewtopic.php?t=\\1'),
)

URLS = []


def URLtransform(inUrl, kind):
    LOGGER.debug("URL Transform: {} : {}".format(kind, inUrl))
    for regexp, replace in URL_MATCHES:
        match = re.match(regexp, inUrl)
        if match:
            inUrl = re.sub(regexp, replace, inUrl)
    return inUrl
    #

def URLtransform_with_check(inUrl, kind):
    LOGGER.debug("URL Transform: {} : {} : {}".format(kind, URLcheck(inUrl), inUrl))
    for regexp, replace in URL_MATCHES:
        match = re.match(regexp, inUrl)
        if match:
            inUrl = re.sub(regexp, replace, inUrl)
    check = URLcheck(inUrl)
    URLS.append((inUrl, check))
    if check:
        return inUrl
    else:
        return "http://forum.tntcity.org"
    #


# ########################################

def unconvert_residuals(pid, match):
    global HAVE_RESIDUAL
    residual = match.group(0)
    RESIDUALS.append( [ pid, residual, None, None ])
    HAVE_RESIDUAL = True
    LOGGER.error("REMOVE RESIDUAL FROM {}: {}".format(pid, residual))
    return residual


def unconvert_cita(pid, match):
    pre, text, post = match.groups()
    label = None
    m = re.search(r'(?msi)<!--startLabel-->(.*?)<!--endLabel-->', pre)
    if m:
        label = m.group(1)
    return "[cita" + ("={}".format(label) if label else "") + "]" + text + "[/cita]"


def unconvert_me(pid, match):
    name, text = match.groups()
    text = re.sub("<span(\d+) class='ME'><center>(.+?)</center></span\1>", "\\1", text)
    text = re.sub("$name", "", text)
    return '[me=' + name + ']' + text + '[/me]'


def unconvert_size(pid, match):
    size = int(match.group(1))
    if size > 24:
        size = 24
    elif size < 9:
        size = 9
    return str(size)


def unconvert_font(pid, match):
    FONTS = ["MONOSPACE", "SERIF", "SANS-SERIF", "CURSIVE",
             "ARIAL", "TAHOMA", "GEORGIA", "FIXEDSYS"]
    font = match.group(1)
    if font.upper() not in FONTS:
        font = FONTS[0]
    return font.upper()


def unconvert_spoiler(pid, match):
    content = match.group(0)
    parts = re.split('<!--SpLab-->', content)
    un_label = parts[1] if len(parts) > 1 else ""
    parts = re.split('<!--SpData-->', content)
    un_spoiler = parts[1]
    if un_label != "":
        un_spoiler = "\n[spoiler=" + un_label + "]\n" + un_spoiler + "\n[/spoiler]\n"
    else:
        un_spoiler = "\n[spoiler]\n" + un_spoiler + "\n[/spoiler]\n"
    return un_spoiler


def unconvert_sql(pid, match):
    sql = match.group(2)
    sql = sql.decode('string_escape')
    while re.match("(?:is)<span(\d+) style='.+?'>(.+?)</span\1>", sql):
        sql = re.sub("(?is)<span(\d+) style='.+?'>(.+?)</span\1>", "\\1", sql)
    sql = re.sub("\s*$", "", sql)
    return '[sql]' + sql + '[/sql]'


def unconvert_htm(pid, match):
    html = match.group(2)
    html = html.decode('string_escape')
    while re.match("(?:is)<span(\d+) style='.+?'>(.+?)</span\1>", html):
        html = re.sub("(?is)<span(\d+) style='.+?'>(.+?)</span\1>", "\\1", html)
    html = re.sub("\s*$", "", html)
    return '[html]' + html + '[/html]'


def unconvert_flash(pid, match):
    f_arr = match.group(1)
    f_arr = f_arr.split("+")
    return '[flash=' + f_arr[0] + ',' + f_arr[1] + ']' + f_arr[2] + '[/flash]'


def unconvert_youtube(pid, match):
    yout = match.group(1)
    return '[youtube=' + re.sub('|', '-', yout) + ']'


def unconvert_url(pid, match):
    grp = match.groups()
    if grp[0] == "img":
        return "[img]" + URLtransform(grp[1], "IMG") + "[/img]"
    elif grp[0] in ("http://", "https://", "ftp://", "news://"):
        url = URLtransform("{}{}".format(grp[0], grp[1]), "LNK")
        return "[url={}]{}[/url]".format(url, grp[2])
    elif grp[0] in ("./", "/"):
        url = URLtransform("{}{}".format(SITE_URL, grp[1]), "LOC")
        return "[url={}]{}[/url]".format(url, grp[2])
    LOGGER.error("ERROR-URL: {} | {} > {}".format(grp[0], grp[1], match.group(0)))
    return "[url={}]{}[/url]".format(grp[1], grp[2])
    # raise "ErrorUrl"


TRANSFORM_STEPS = [
    # BR
    ["<br></br>", "<br/>", False],
    ["<br>", "<br/>", False],
    # ["<br/>", "\n", False],
    # EMOJ
    ["<!--emo\&(.+?)-->.+?<!--endemo-->", "\\1", False],
    # SQL
    ["(?is)<!--sql-->(.+?)<!--sql1-->(.+?)<!--sql2-->(.+?)<!--sql3-->", unconvert_sql, False],
    # HTML
    ["<!--html-->(.+?)<!--html1-->(.+?)<!--html2-->(.+?)<!--html3-->",  unconvert_htm, False],
    # FLASH
    ["<!--Flash (.+?)-->.+?<!--End Flash-->", unconvert_flash, False],
    # IMG
    [r"(?is)<(img) .*?src=[\"'](\S+?)['\"].*?()/>", unconvert_url, False],
    [r"(?is)<(img) .*?src=[\"'](\S+?)['\"].*?>(.*?)</img>", unconvert_url, False],
    # EMAIL
    ["<a href=[\"']mailto:(.+?)['\"]>(.+?)</a>", "[email=\\1]\\2[/email]", False],
    # URL
    ["<a href=[\"'](http://|https://|ftp://|news://|\./|/)?(\S+?)['\"].*?>(.+?)</a>",
     unconvert_url, False],
    # IMDB
    ["(?ms)<!--ImdbBegin(.+?)-->(.+?)<!--ImdbEnd(.+?)-->", '[imdb=\\1]', False],
    # FREEDB
    ["(?ms)<!--freedbBegin(.+?)-->(.+?)<!--freedbEnd(.+?)-->", '[freedb=\\1]', False],
    # YOUTUBE
    ["(?msi)<!--YoutubeBegin(.+?)-->(.+?)<!--YoutubeEnd(.+?)-->",  unconvert_youtube, False],
    # ALIGN
    ["(?ms)<!--AlignTagStart--><div\ align='(.+?)'>(.+?)</div><!--AlignTagEnd-->",
     '\n[align=\\1]\n\\2\n[/align]\n', False],
    # DONATE
    ["(?ms)<!--donateBegin-->(.+?)<!--donateEnd-->", '[donate]', False],
    # SPOILER
    ["(?ms)<!--SpoilerBegin-->(.+?)<!--SpoilerEnd-->", unconvert_spoiler, False],
    # CITA
    [r"(?msi)<!--CitaBegin-->(.+?)<!--CitaTextStart-->(.+?)<!--CitaTextEnd-->(.+?)<!--CitaEnd-->",
        unconvert_cita, False],
    # QUOTE
    [r"<!--QuoteBegin-->(.+?)<!--QuoteEBegin-->", '[quote]', False],
    [r"<!--QuoteBegin-{1,2}([^>]+?)\+([^>]+?)-->(.+?)<!--QuoteEBegin-->", "[quote=\\1,\\2]", False],
    [r"<!--QuoteBegin-{1,2}([^>]+?)\+-->(.+?)<!--QuoteEBegin-->", "[quote=\\1]", False],
    [r"<!--QuoteEnd-->(.+?)<!--QuoteEEnd-->", '[/quote]', False],
    # CODE
    ["<!--c1-->(.+?)<!--ec1-->", '[code]', False],
    ["<!--c2-->(.+?)<!--ec2-->", '[/code]', False],
    # I / B / S / U
    ["(?is)<i>(.+?)</i>", "[i]\\1[/i]", False],
    ["(?is)<b>(.+?)</b>", "[b]\\1[/b]", False],
    ["(?is)<s>(.+?)</s>", "[s]\\1[/s]", False],
    ["(?is)<u>(.+?)</u>", "[u]\\1[/u]", False],
    # LIST
    ["(\n){0,}<ul>", "\\1[list]", False],
    ["(\n){0,}<ol type='(a|A|i|I|1)'>", "\\1[list=\\2]\n", False],
    ["(\n){0,}<li>", "\n[*]", False],
    ["(\n){0,}</ul>(\n){0,}", "\n[/list]\\2", False],
    ["(\n){0,}</ol>(\n){0,}", "\n[/list]\\2", False],
    # ME
    ["<!--me&(.+?)-->(.+?)<!--e--me-->", unconvert_me, False],
    # SPAN
    [r"(?mis)<span(\d*) style=['\"](.+?)['\"]>(.+?)</span\1>", "[span\\1 \\2]\\3[/span\\1]", True],
    # SPAN-Color
    [r"(?s)\[span(\d*) color:(.+?)\](.+?)\[/span\1]", "[color=\\2]\\3[/color]", True],
    # SPAN-Size
    [r"(?s)\[span(\d*) font-size:(.+?)pt.*?\](.+?)\[/span\1]", "[size=\\2]\\3[/size]", True],
    [r"(?s)(?<=\[size=)(\d+)", unconvert_size, False],
    # SPAN-Font
    [r"(?s)\[span(\d+) font-family:(.+?)\](.+?)\[/span\1]", "[font=\"\\2\"]\\3[/font]", True],
    [r"(?s)(?<=\[font=\")(.*?)(?=\")", unconvert_font, False],
    # TIDY-UP
    ["(?is)(\[/quote\])\s*?<br/?>\s*", "\\1\n", False],
    ["(?i)<!--edit\|.+?\|.+?-->", "", False],
    ["</li>", "",  False],
    ["&#153;", "(tm)", False],
    #     # HTML
    ["&#39;", "'", False],
    # BR
    ["<br/>", '\n', False],
    ["(?msi)<br>(.*?)</br>", '\n', False],
    ["</br>", '\n', False],
    [r"</?\w+.*?>", unconvert_residuals, False],

]


def unconvert_post(pid, post, steps=TRANSFORM_STEPS):
    old = text = post
    n = 1
    for regexp, subst, rep in steps:
        LOGGER.debug('regexp:' + regexp)
        if rep:
            text = unconvert_post_multi(pid, text, regexp, subst)
        else:
            text = unconvert_post_single(pid, text, regexp, subst)
        old = text
        n += 1
    return text


def unconvert_post_multi(pid, text, regexp, subst):
    LOGGER.debug('multi')
    lasttxt = None
    N = 10
    while lasttxt != text:
        LOGGER.debug('Loop on pid {} & {}'.format(pid,N))
        lasttxt = text
        text = unconvert_post_single(pid, text, regexp, subst)
        N -= 1
        if N==0:
            RESIDUALS.append( [pid, None, None, None]) 
            HAVE_RESIDUAL = True
            LOGGER.error('Break Loop on pid {}'.format(pid))
            break
    return text


def unconvert_post_single(pid, text, regexp, subst):
    if callable(regexp):
        LOGGER.debug('single-callable-regext')
        text = regexp(pid, text)
    elif callable(subst):
        LOGGER.debug('single-callable-subst '+regexp)
        match = re.search(regexp, text)
        if match:
            LOGGER.debug('A-MATCHED:{}:{:100}'.format(regexp, match.group(0)))
            return_string = subst(pid, match)
            text = re.sub(regexp, return_string, text)
    else:
        LOGGER.debug('single-match')
        match = re.search(regexp, text)
        if match:
            LOGGER.debug('B-MATCHED-IN:{}:{:100}'.format(regexp, match.group(0)))
            text = re.sub(regexp, subst, text)
            # LOGGER.debug('B-MATCHED-OU:{:100}'.format(text))
    LOGGER.debug('~single')
    return text

def html2bbcode(trn, post):
    global HAVE_RESIDUAL
    pid = trn._record['pid']
    LOGGER.debug('html2bbcode pid {}'.format(pid))
    DONE_POST.append( [pid, False])
    HAVE_RESIDUAL = False
    LOGGER.setLevel(logging.WARN)
    new_post = unconvert_post(pid, post)
    if HAVE_RESIDUAL:
        RESIDUALS[-1][2] = post
        RESIDUALS[-1][3] = new_post
    DONE_POST[-1][1] = True
    return stringify(trn, new_post)
