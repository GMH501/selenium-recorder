import os
import shlex
from subprocess import Popen
import time
from signal import SIGTERM

from psutil import Process



print("Starting recording..")
startCmd = "ffmpeg -y -f x11grab -video_size 1360x1020 -r 15 -i selenium:99.0 -codec:v libx264 -preset ultrafast -pix_fmt yuv420p /videos/video-123.mp4"
startArgs = shlex.split(startCmd)
## STARTING PROCESS
parentProcess = Popen(startCmd, shell=True)
parentPid = parentProcess.pid
print('Writing PID {} to file ffmpeg.pid'.format(parentPid))
## WRITING PID
with open('ffmpeg.pid', 'w') as f:
    f.write(str(parentPid))
## READING PID
with open('ffmpeg.pid', 'r') as pidFile:
    parentPid = pidFile.read()
print('Read PID {} from file ffmepg.pid'.format(parentPid))
parentPid = int(parentPid)
time.sleep(5)
# stopCmd = "ps -aux | grep ffmpeg | awk '{print }' | xargs -I {} kill -s 15 {}"
print("Killing process..")
parentProcess = Process(parentPid)
## KILLING PROCESS
kill_process = [os.kill(childPid.pid, SIGTERM) for childPid in parentProcess.children() if childPid.name() == 'ffmpeg']
os.system("rm -f ffmpeg.pid")