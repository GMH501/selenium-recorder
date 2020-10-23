import random
import string
import shlex
import functools
from functools import wraps
from datetime import datetime

from flask import redirect, session, url_for


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

def randomChars(y):
    return ''.join(random.choice(string.ascii_lowercase) for x in range(y))


def startCmd():
    cmd = "/usr/local/bin/ffmpeg -y -nostdin -f x11grab -video_size 1360x1020 -r 15 -i selenium:99.0 -codec:v libx264 -preset ultrafast -pix_fmt yuv420p /opt/bin/tester/tester/static/videos/rec_{}.mp4".format(datetime.now().strftime("%m%d%Y_%H%M%S"))
    return shlex.split(cmd)