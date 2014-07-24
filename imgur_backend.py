#!/usr/bin/python

from base64 import b64encode, b64decode
from zlib import compress, decompress
import json
import random
import requests
import string
import struct
import stepic
import sys
from PIL import Image
from StringIO import StringIO

username = "pokeman2014"
password = "pikachu0724"
client_id = "a0af21a237b8ae7"
client_secret = "42d3486f78b21c616f72ed55bbba4dc771b0cec8"
album_id = "aAXVT"
album_deletehash = "mmUO2qw9AJNlgel"
HEADERS = {"Authorization": "Client-ID " + client_id,
           "Accept": "application/json",
           "Content-Type": "application/json"}

def upload_image(filename):
    url = "https://api.imgur.com/3/image"
    encoded_image = b64encode(open(filename, 'rb').read())
    #print open(filename).read()
    #print encoded_image
    data = {"image": encoded_image,
            "album": album_deletehash,
            "type": "base64"}
    resp = requests.post(url, headers=HEADERS, data=json.dumps(data))
    return resp

def get_and_decode_image(img_link):
    resp = requests.get(img_link)
    #print resp.content
    img = Image.open(StringIO(resp.content))
    return decompress(stepic.decode(img))

text = open(sys.argv[1]).read()
print text
encoded_image = stepic.encode(Image.open("hobbes.png"), compress(text))
encoded_image.save("tmp.png")

resp = upload_image("tmp.png")
resp_data = json.loads(resp.content)
#print resp_data

result = get_and_decode_image(resp_data["data"]["link"])
print result

def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#new_img = stepic.encode(Image.open("hobbes.png"), string_generator(10000))
#new_img.save("fancy.png")

#print stepic.decode(Image.open("tmp.png"))
