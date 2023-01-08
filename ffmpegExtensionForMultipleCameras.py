# Version for working Arduino + Motion sensors

import serial
import subprocess
import threading
import time
import os
import psutil
import signal

# ================================================================
# ---------< Define critical variables before main loop >---------
# ================================================================

# ---> Set up the serial connection <---
ser = serial.Serial('/dev/ttyACM0', 9600)
line = ser.readline()

# ---> Main camera paths <---
# If cams not matching, use command and rewrite the cam paths
# "v4l2-ctl --list-devices"
cam1 = '/dev/video0' + ' '
cam2 = '/dev/video2' + ' '
cam3 = '/dev/video4' + ' '
cam4 = '/dev/video6' + ' '
# If no video loopback, use command
# "sudo modprobe v4l2loopback video_nr=1"
# Then check the path of the new video loopback and rewrite the virtual_cam path
virtual_cam = '/dev/video17'

# ---> Define camera syntax ready for end-process <---
icam1 = '-thread_queue_size 100 -i ' + cam1
icam2 = '-thread_queue_size 100 -i ' + cam2
icam3 = '-thread_queue_size 100 -i ' + cam3
icam4 = '-thread_queue_size 100 -i ' + cam4


# ---> The process is starting, there is no Running process yet <---
running_process = ''

# ---> Create booleans for 5sec "flag" timer <---
active1 = False
active2 = False
active3 = False
active4 = False

# ---> Define placeholders for active, held or disabled cameras for end-process syntax <---
# "p" variables are being filled while the cam is active or held by flag
p1 = ''
p2 = ''
p3 = ''
p4 = ''

# ---> Placeholder for Activated Motion Sensors <---
sum = 0

# ---> Default horizontal position for def_process <---
slot = '[0:v:0][1:v:0][2:v:0][3:v:0]'

# ---> Main loop <---
while True:

  # ---> Check if the serial line matches a specific pattern <---
  # Define variable to decode serial input
  line_str = line.decode('utf-8')

  # Camera 1.
  if "cam1" in line_str: # When cam1 phraze found in serial arduino output
    active1 = True # Gives "flag" to camera
  else:
    active1 = False # cam1 starts to lose it's flag

  # Camera 2.
  if "cam2" in line_str:
    active2 = True
  else:
    active2 = False

  # Camera 3.
  if "cam3" in line_str:
    active3 = True
  else:
    active3 = False

  # Camera 4.
  if "cam4" in line_str:
    active4 = True
  else:
    active4 = False

  # ---> Run countdown to check if dropped flags will get regained <--- 
  if active1 == False or active2 == False or active3 == False or active4 == False:
    for i in range(20, 0, -1):
      line_str = line.decode('utf-8')
      if active1 == False:
          if "cam1" in line_str: # If camera was found, tag the boolean as true, the countdown cancels
              active1 = True # Renew flag
              print('Cam1 found') # Control output when cam1 not found
      if active2 == False:
          if "cam2" in line_str:
              active2 = True 
              print('Cam2 found')
      if active3 == False:
          if "cam3" in line_str:
              active3 = True 
              print('Cam3 found')
      if active4 == False:
          if "cam4" in line_str:
              active4 = True 
              print('Cam4 found')

  # ---> Check if flag active or dropped <----
  if active1:
    p1 = icam1 # Add camera path to end-process
    sum += 1 # Reserve a slot for cam in final video output
  else:
    p1 = '' # Remove camera path from end-process

  if active2:
    p2 = icam2
    sum += 1
  else:
    p2 = ''
  
  if active3:
    p3 = icam3
    sum += 1
  else:
    p3 = ''

  if active4:
    p4 = icam4
    sum += 1
  else:
    p4 = ''


  # ---> Control value for active Motion sensors <---
  print('There are ', sum, ' motion sensors activated')

  # ---> Define how many camera slots are needed <---
  if sum == 1:
    slot = '[0:v:0]'
  elif sum == 2:
    slot = '[0:v:0][1:v:0]'
  elif sum == 3:
    slot = '[0:v:0][1:v:0][2:v:0]'
  elif sum == 4:
    slot = '[0:v:0][1:v:0][2:v:0][3:v:0]'
  elif sum == 0:
    slot = '[0:v:0][1:v:0][2:v:0][3:v:0]'
    sum = 4 # Important for end-process

  

  # ---> Default position of all cameras <---
  def_process = 'ffmpeg ' + icam1 + icam2 + icam3 + icam4 + '-filter_complex "[0:v:0][1:v:0][2:v:0][3:v:0]hstack=inputs=4[outv]" -map "[outv]" -f v4l2 ' + virtual_cam

  # ---> Currently used cameras <---
  # If no movement on any cameras, show default position
  if p1 == '' and p2 == '' and p3 == '' and p4 == '':
    prep_process = def_process
  # Exception for single camera
  elif sum == 1:
    prep_process = 'ffmpeg ' + p1 + p2 + p3 + p4 + ' -f v4l2 ' + virtual_cam
  # Multiple cameras are active
  else:
    prep_process = 'ffmpeg ' + p1 + p2 + p3 + p4 +  ' -filter_complex "' + slot + 'hstack=inputs=' + str(sum) + '[outv]" -map "[outv]" -f v4l2 ' + virtual_cam

  # If the process started in the past is not equal to the new process
  if prep_process != running_process:
    # Kill process that contains "ffmpeg" phraze in description
    for proc in psutil.process_iter():
      if proc.name() == "ffmpeg":
        os.kill(proc.pid, signal.SIGKILL)
    # Run new process
    time.sleep(1)
    subprocess.run(["gnome-terminal", "-x", "bash", "-c", prep_process]) # Opens new terminal window that starts the new video output
    print(prep_process) # Control output of the process syntax 

    # The most recently started process gets transformed into Running process
    running_process = prep_process

  # If no movement sensor changes -> no layout changes
  elif prep_process == running_process:
    print('No changes')

  sum = 0 # Reset the slot placehold counter
  time.sleep(3) # Three secound pause for cathing a breath