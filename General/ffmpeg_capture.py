#! /usr/bin/python3

import datetime
import subprocess
import time

cmd1 = ['slop', "--format=%x %y %h %w"]
cmd2 = ["xrandr", "-d", ":0"]
cmd3 = ["grep", "*"]

proc1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
output1, _ = proc1.communicate()
proc1.stdout.close()
one, two, tre, fou = (output1.decode('utf-8')).split()
if (int(tre) % 2) != 0:
    tre = str(int(tre) - 1)
if (int(fou) % 2) != 0:
    fou = str(int(fou) - 1)
#print("Dim=%s, %s, %s, %s" % (one, two, tre, fou))

proc2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE)
proc3 = subprocess.Popen(cmd3, stdin=proc2.stdout, stdout=subprocess.PIPE)
proc2.stdout.close()
output3, _ = proc3.communicate()
resolute = (output3.decode("utf-8")).split()[0]
# width, height = resolute.split("x")
print("Display size: %s" % resolute)
print("Output size: %sx%s" % (fou, tre))

for delay in reversed(range(6)):
    print(("Staring in %s... " % delay), end="\r")
    time.sleep(0.99)
print("Recording Now" + (" " * 10))

cmd4 = [
"ffmpeg", 
"-thread_queue_size", "1536",  
# "-loglevel","fatal", "-stats",
# Capture PulseAudio stream here.
"-f", "alsa", 
# "-ac", "2",
"-channel_layout", "stereo",
"-i", "pulse",
# Capture actions on screen through x11.
"-f", "x11grab",
"-s", resolute,
"-r", "30", 
"-i", ":0.0",
# Record for this many hours/minutes/seconds.
"-t", "00:00:10",
"-profile:v", "baseline",
# Cutting video to your selection.
#                                   o_w  o_y   x    y
"-filter:v", ("crop=%s:%s:%s:%s" % (fou, tre, one, two)),
# H.264 options go here.
"-c:v", "libx264", 
"-preset", "medium", 
"-pix_fmt", "yuv420p",
# Encoding audio here.
"-c:a", "libmp3lame", 
"-b:a", "128k",
# Experimental option(s) here.
"-movflags", "faststart",
# Finally saving file to name below. 
("cast-" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".mp4")]
 
proc2 = subprocess.run(cmd4)
print("Done")
