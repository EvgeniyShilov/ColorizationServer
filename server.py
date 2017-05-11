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

run(host='localhost', port=8080, debug=True)
