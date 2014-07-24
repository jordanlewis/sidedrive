#!/usr/bin/python

import mechanize
import re
import sys
import uuid
from base64 import b64encode
from zlib import compress
import struct

username = "hodor1988"
password = "hodorhodor"

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
def tweet_text(b, username, text):
    tweet_ids = []
    for i in xrange(0, len(text), 140):
        chunk = text[i:i+140]
        tweet_id = tweet_chunk(b, chunk)
        print "Tweeted %s to %s:" % (chunk, tweet_id)
        tweet_ids.append(tweet_id)

    if len(tweet_ids) == 1:
        print "Done! root tweet is %s" % tweet_ids[0]
        return tweet_ids[0]

    tweet_refs = []
    for tweet_id in tweet_ids:
        encoded = b64encode(struct.pack(">Q", int(tweet_id)))
        tweet_ref = "!" + b64encode(compress(username + "|" + encoded))
        tweet_refs.append(tweet_ref)
    print "Made %d tweet ids... tweeting %s now" % (len(tweet_ids), "".join(tweet_refs))
    return tweet_text(b, username, "".join(tweet_refs))

b = mechanize.Browser()
login(b, username, password)
text = open(sys.argv[1]).read() + str(uuid.uuid4())
compressed = b64encode(compress(text))

print tweet_text(b, username, compressed)
