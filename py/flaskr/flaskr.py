# Python2.5+
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from random import SystemRandom
from base64 import b64encode

import runner

rng = SystemRandom()

# configuration
DEBUG = False
SECRET_KEY = b64encode(str(rng.getrandbits(256)))
USERNAME = b64encode(str(rng.getrandbits(256)))
PASSWORD = b64encode(str(rng.getrandbits(256)))

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET'])
def classify_upload():
    if request.method == 'GET':
        filename = request.args.get('fileid') or None
        if filename is not None:
            return runner.class_img(filename)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
