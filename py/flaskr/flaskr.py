
# The MIT License (MIT)
#
# Copyright (c) 2016 Maeve Kennedy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
