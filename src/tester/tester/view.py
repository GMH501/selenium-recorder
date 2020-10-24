import os
from subprocess import Popen
from signal import SIGTERM
from datetime import datetime
import subprocess
from random import randint  # DEBUG

from psutil import Process
from flask import Flask, jsonify, render_template, url_for, session, redirect, request

from tester.helpers import *

def index():
    return render_template('index.html')


def get_length(filename):
    try:
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        result = float(result.stdout)
        minutes = result / 60
        if int(minutes) > 0:
            seconds = result // 60
            return "{} Minutes, {} Seconds".format(int(minutes), int(seconds))
        else:
            return "{} Seconds".format((int(result)))
    except:
        return "0 Seconds"


def start():
    # return jsonify({'stopped': 'false'}), 202
    if os.path.exists('/opt/bin/ffmpeg.pid'):
        with open('/opt/bin/ffmpeg.pid', 'r') as f:
            parentPid = f.read()
        parentProcess = Process(int(parentPid))
        return jsonify({'started': 'false', 'status': parentProcess.status()}), 202
    parentProcess = Popen(startCmd(), shell=False)
    parentPid = parentProcess.pid
    with open('/opt/bin/ffmpeg.pid', 'w') as f:
        f.write(str(parentPid))
    parentProcess = Process(parentPid)
    return jsonify({'started': 'true', 'status': parentProcess.status()}), 200


def status():
    # return jsonify({'stopped': 'false'}), 202
    if os.path.exists('/opt/bin/ffmpeg.pid'):
        return jsonify({'status': 'runnig'}), 200
    else:
        return jsonify({'status': 'not runnig'}), 202


def stop():
    #return jsonify({'stopped': 'false'}), 200
    try:
        with open('/opt/bin/ffmpeg.pid', 'r') as pidFile:
            parentPid = pidFile.read()
    except:
            return jsonify({'stopped': 'false'}), 202
    parentPid = int(parentPid)
    parentProcess = Process(parentPid)
    os.kill(parentPid, SIGTERM)
    os.system("rm -f /opt/bin/ffmpeg.pid")
    return jsonify({'stopped': 'true'}), 200

def videos():
    data = {"data": []}
    with os.scandir(r'/opt/bin/tester/tester/static/videos') as dir_contents:
        for entry in dir_contents:
            name = entry.name
            completeName = '/opt/bin/tester/tester/static/videos/' + name
            if 'mp4' in name:
                info = entry.stat()
                size = info.st_size
                mtime = info.st_mtime
                date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d-%H:%M')
                data["data"].append({"name" : name, "size": round(size / 1024 / 1024, 2), "date": date, "duration": get_length(completeName)})
    return jsonify(data)


