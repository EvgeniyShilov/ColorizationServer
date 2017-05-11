#!/usr/bin/python

from bottle import *
from neuralnet import colorize

@post('/load')
def load():
    img = request.body.read()
    id = request.get_header("id")
    token = request.get_header("token")
    f = open(".\\storage\\input\\" + id + ".png", "wb")
    f.write(img.decode('base64'))
    f.close()
    colorize.colorize(".\\storage\\input\\" + id + ".png", ".\\storage\\output\\" + id + ".png", token)

@get("/get")
def get():
    id = request.get_header("id")
    f = open(".\\storage\\output\\" + id + ".png", "rb")
    img = f.read().encode("base64")
    f.close()
    return img

run(host='172.17.0.2', port=8080, debug=True)
