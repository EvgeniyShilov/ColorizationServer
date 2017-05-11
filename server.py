#!/usr/bin/python

from bottle import *

@post('/load')
def load():
    img = request.body.read()
    id = request.get_header("id")
    f = open(id + ".png", "wb")
    f.write(img.decode('base64'))
    f.close()

@get("/get")
def get():
    id = request.get_header("id")
    f = open(id + ".png", "rb")
    img = f.read().encode("base64")
    f.close()
    return img

run(host='172.17.0.2', port=8080, debug=True)
