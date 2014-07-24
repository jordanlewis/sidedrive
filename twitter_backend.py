#!/usr/bin/python

import mechanize
import re
import sys
import uuid
import urllib2
from base64 import b64encode, b64decode
from zlib import compress, decompress
import struct

from backends import Backend

USERNAME = "hodor1988"
PASSWORD = "hodorhodor"

def login(b, username, password):
    b.open("http://twitter.com")
    b.form = [f for f in b.forms() if f.attrs["class"] == "t1-form signin"][0]
    b.form.controls[0].value = username
    b.form.controls[1].value = password
    b.submit()

def tweet_chunk(b, chunk):
    if len(chunk) > 140:
        raise Exception("too long tweet chunk")
    b.open("https://twitter.com/intent/tweet?text=%s" % chunk)
    b.form = [f for f in b.forms() if f.attrs.get("id", None) == "update-form"][0]
    resp = b.submit().read()
    tweet_id = re.search("/intent/tweet/complete\?latest_status_id=(\d+)", resp).groups()[0]
    return tweet_id

#text is represented as arbitrarily deep n-ary trees of tweets.
#internal nodes consist of !-separated compressed tweet ids
def tweet_text(b, username, text, index=False):
    chunks = []
    if index:
        # if we're an index we have can't split inside a ref
        cur_chunk = ""
        for ref in text.split("!"):
            if len(cur_chunk) + 1 + len(ref) > 140:
                chunks += cur_chunk
                cur_chunk = ""
            if cur_chunk:
                cur_chunk += "!"
            cur_chunk += ref
        chunks.append(cur_chunk)
    else:
        for i in xrange(0, len(text), 140):
            chunks.append(text[i:i+140])

    tweet_ids = []
    for chunk in chunks:
        tweet_id = tweet_chunk(b, chunk)
        print "Tweeted %s to %s:" % (chunk, tweet_id)
        tweet_ids.append(tweet_id)

    if len(tweet_ids) == 1:
        print "Done! root tweet is %s" % tweet_ids[0]
        return username, tweet_ids[0]

    tweet_refs = []
    for tweet_id in tweet_ids:
        encoded = b64encode(struct.pack(">Q", int(tweet_id)))
        tweet_ref = b64encode(compress(username + "|" + encoded))
        tweet_refs.append(tweet_ref)
    print "Made %d tweet ids... tweeting %s now" % (len(tweet_ids), "!".join(tweet_refs))
    return tweet_text(b, username, "!".join(tweet_refs), index=True)

def read_tweet(username, tweet_id):
    b = mechanize.Browser()
    page = urllib2.urlopen("http://twitter.com/%s/status/%s" % (username, tweet_id)).read()
    text = re.search("js-tweet-text tweet-text\">(.*)</p>", page).groups()[0]
    print "found text for tweet %s:%s: %s" % (username, tweet_id, text)
    return text

def read_tweet_tree(username, root_tweet_id):
    root_text = read_tweet(username, root_tweet_id)
    if "!" in root_text:
        refs = root_text.split("!")
        ret = ""
        for ref in refs:
            print ref
            username, encoded = decompress(b64decode(ref)).split("|")
            tweet_id = str(struct.unpack(">Q", b64decode(encoded))[0])
            ret += read_tweet_tree(username, tweet_id)
        return ret
    else:
        return root_text

class TwitterBackend(Backend):

    def __init__(self):
        b = mechanize.Browser()
        login(b, USERNAME, PASSWORD)
        self.b = b

    def get(self, ref_list):
        tweet_id = ref_list[0]
        return decompress(b64decode(read_tweet_tree(USERNAME, tweet_id)))[:-36]

    def store(self, data):
        compressed = b64encode(compress(data))
        _, tweet_id = tweet_text(b, USERNAME, compressed)
        return tweet_id

if __name__=="__main__":
    b = mechanize.Browser()
    login(b, USERNAME, PASSWORD)
    text = open(sys.argv[1]).read() + str(uuid.uuid4())
    compressed = b64encode(compress(text))

    username, tweet_id = tweet_text(b, username, compressed)
    print username, tweet_id

    print "fetching result..."

    print decompress(b64decode(read_tweet_tree(username, tweet_id)))[:-36]
