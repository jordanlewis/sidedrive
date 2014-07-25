#!/usr/bin/python

from base64 import b64encode, b64decode
from zlib import compress, decompress
import json
import random
import string
import struct
import stepic
import sys
import urllib, urllib2
from PIL import Image
from StringIO import StringIO

from backends import Backend

username = "pokeman2014"
password = "pikachu0724"
client_id = "a0af21a237b8ae7"
client_secret = "42d3486f78b21c616f72ed55bbba4dc771b0cec8"
album_id = "aAXVT"
album_deletehash = "mmUO2qw9AJNlgel"
HEADERS = {"Authorization": "Client-ID " + client_id,
           "Accept": "application/json",
           "Content-Type": "application/json"}

def upload_image(image_data):
    url = "https://api.imgur.com/3/image"
    encoded_image = b64encode(image_data)
    data = {"image": encoded_image,
            "album": album_deletehash,
            "type": "base64"}
    resp = urllib2.urlopen(urllib2.Request(url, json.dumps(data), HEADERS)).read()
    return resp

def get_and_decode_image(img_link):
    resp = urllib2.urlopen(img_link)
    #print resp.content
    img = Image.open(StringIO(resp.read()))
    return decompress(stepic.decode(img))

if __name__ == "__main__":
    text = open(sys.argv[1]).read()
    print text
    encoded_image = stepic.encode(Image.open("hobbes.png"), compress(text))
    output = StringIO()
    encoded_image.save(output, format="png")
    resp = upload_image(output.getvalue())

    resp_data = json.loads(resp)
    #print resp_data

    result = get_and_decode_image(resp_data["data"]["link"])
    print result

def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#new_img = stepic.encode(Image.open("hobbes.png"), string_generator(10000))
#new_img.save("fancy.png")

#print stepic.decode(Image.open("tmp.png"))

class ImgurBackend(Backend):

    def get(self, ref_list):
        link = ref_list[0]
        return get_and_decode_image(link)

    def store(self, data):
        encoded_image = stepic.encode(Image.open("hobbes.png"), compress(data))
        output = StringIO()
        encoded_image.save(output, format="png")
        resp = upload_image(output.getvalue())
        resp_data = json.loads(resp)
        return resp_data["data"]["link"]
