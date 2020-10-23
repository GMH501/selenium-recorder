import os
import shlex
from subprocess import Popen
import random
import string
from signal import SIGTERM

from psutil import Process
from flask import Flask, jsonify


app = Flask(__name__)


def randomChars(y):
    return ''.join(random.choice(string.ascii_lowercase) for x in range(y))


def startCmd():
    cmd = "/usr/local/bin/ffmpeg -y -nostdin -f x11grab -video_size 1360x1020 -r 15 -i selenium:99.0 -codec:v libx264 -preset ultrafast -pix_fmt yuv420p /videos/rec_{}.mp4".format(randomChars(5))
    return shlex.split(cmd)

@app.route('/start')
def start():
    if os.path.exists('/opt/bin/ffmpeg.pid'):
        with open('/opt/bin/ffmpeg.pid', 'r') as f:
            parentPid = f.read()
        parentProcess = Process(int(parentPid))
        return jsonify({'started': 'false', 'status': parentProcess.status()})
    parentProcess = Popen(startCmd(), shell=False)
    parentPid = parentProcess.pid
    with open('/opt/bin/ffmpeg.pid', 'w') as f:
        f.write(str(parentPid))
    parentProcess = Process(parentPid)
    return jsonify({'started': 'true', 'status': parentProcess.status()})

@app.route('/stop')
def stop():
    try:
        with open('/opt/bin/ffmpeg.pid', 'r') as pidFile:
            parentPid = pidFile.read()
    except:
            return jsonify({'stopped': 'false'})
    parentPid = int(parentPid)
    parentProcess = Process(parentPid)
    os.kill(parentPid, SIGTERM)
    os.system("rm -f /opt/bin/ffmpeg.pid")
    return jsonify({'stopped': 'true'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)