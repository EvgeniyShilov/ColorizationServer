#!/usr/bin/python

from threading import *
from bottle import *
from neuralnet import colorization

@post('/load')
def load():
    input_path = "./storage/input/"
    img = request.body.read()
    id = request.get_header("id")
    token = request.get_header("token")
    f = open(input_path + id + ".png", "wb")
    f.write(img.decode('base64'))
    f.close()
    t = threading.Thread(target=colorization.colorize, args=(id, token))
    t.start()

@get("/get")
def get():
    output_path = "./storage/output/"
    id = request.get_header("id")
    img_out = output_path + id + ".png"
    f = open(img_out, "rb")
    img = f.read().encode("base64")
    f.close()
    return img

run(host='172.17.0.2', port=8080, debug=True)
