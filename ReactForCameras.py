import serial
import subprocess
import threading
import time
import os
import psutil
import signal

# Set up the serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)

# Define camers

cam1 = '/dev/video0'
cam2 = '/dev/video2'
cam3 = '/dev/video4'
cam4 = '/dev/video6'
virtual_cam = '/dev/video8'

# Define camera syntax ready for process

icam1 = '-thread_queue_size 100 -i ' + cam1
icam2 = '-thread_queue_size 100 -i ' + cam2
icam3 = '-thread_queue_size 100 -i ' + cam3
icam4 = '-thread_queue_size 100 -i ' + cam4


# The process is starting, there is no Running process yet
running_process = ''

# Create booleans for 5sec "flag" timer
actv1 = False
actv2 = False
actv3 = False
actv4 = False

slot = '[0:v:0][1:v:0][2:v:0][3:v:0]'

# Define 5sec "flag" timer
def countdown1():
    # Print the countdown
    for i in range(20, 0, -1):
        print(i + " cam1") # Countdown control output
        if line_str == "cam1\n": # If camera was found, tag the boolean as true, the countdown cancels
            found_cam1 = True 
            print('Cam1 found')
            sum += 1
            break
        else:
            found_cam1 = False # If camera wasn't found after countdown, tag the boolean as false
        time.sleep(.1)
    if found_cam1 == False:
        actv1 = False # Remove camera from output

def countdown2():
    # Print the countdown
    for i in range(20, 0, -1):
        print(i + " cam2") # Countdown control output
        if line_str == "cam2\n": # If camera was found, tag the boolean as true, the countdown cancels
            found_cam2 = True 
            print('Cam2 found')
            sum += 1
            break
        else:
            found_cam2 = False # If camera wasn't found after countdown, tag the boolean as false
        time.sleep(.1)
    if found_cam2 == False:
        actv2 = False # Remove camera from output

def countdown3():
    # Print the countdown
    for i in range(20, 0, -1):
        print(i + " cam3") # Countdown control output
        if line_str == "cam3\n": # If camera was found, tag the boolean as true, the countdown cancels
            found_cam3 = True 
            print('Cam3 found')
            sum += 1
            break
        else:
            found_cam3 = False # If camera wasn't found after countdown, tag the boolean as false
        time.sleep(.1)
    if found_cam3 == False:
        actv3 = False # Remove camera from output

def countdown4():
    # Print the countdown
    for i in range(20, 0, -1):
        print(i + " cam4") # Countdown control output
        if line_str == "cam4\n": # If camera was found, tag the boolean as true, the countdown cancels
            found_cam4 = True 
            print('Cam4 found')
            sum += 1
            break
        else:
            found_cam4 = False # If camera wasn't found after countdown, tag the boolean as false
        time.sleep(.1)
    if found_cam4 == False:
        actv4 = False # Remove camera from output



# Main loop
while True:

  # Read a line of input from the serial port
  line = ser.readline()

  # Decode the line and print it to the console
  line_str = line.decode('utf-8')
  print(line_str)

  # Check if the serial line matches a specific pattern
  # Camera 1.
  if line_str == "cam1\n":
    p1 = cam1
    sum += 1
    actv1 = True # Gives "flag" to camera
  elif line_str != "cam1\n":
    time.sleep(.5)
    if actv1 == True:
        countdown1()

  # Camera 2.
  if line_str == "cam2\n":
    p2 = cam2
    sum += 1
    actv2 = True
  elif line_str != "cam2\n":
    time.sleep(.5)
    if actv2 == True:
        countdown2()

  # Camera 3.
  if line_str == "cam3\n":
    p3 = cam3
    sum += 1
    actv3 = True
  elif line_str != "cam3\n":
    time.sleep(.5)
    if actv3 == True:
        countdown3()

  # Camera 4.
  if line_str == "cam4\n":
    p4 = cam4
    sum += 1
    actv4 = True
  elif line_str != "cam4\n":
    time.sleep(.5)
    if actv4 == True:
        countdown4()

  # Check if motion was found/still active flag

  print('There are ', sum, ' motion sensors activated')

  # Define how many camera slots are needed
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

  if actv1 == False:
    p1 = ''

  if actv2 == False:
    p2 = ''
  
  if actv3 == False:
    p3 = ''

  if actv4 == False:
    p4 = ''
  

  # Default position of all cameras
  def_process = 'ffmpeg ' , icam1 , icam2 , icam3 , icam4 , '-filter_complex "[0:v:0][1:v:0][2:v:0][3:v:0]hstack=inputs=4[outv]" -map "[outv]" -f v4l2 ' , virtual_cam

  # Currently used cameras
  # p - positive_reaction for movement, while movement detected -> camera is being added to the process
  prep_process = 'ffmpeg ' , p1 , p2 , p3 , p4 ,  '-filter_complex "' , slot , 'hstack=inputs=' , sum , '[outv]" -map "[outv]" -f v4l2 ' , virtual_cam

  if prep_process != running_process:
    # Kill process that contains "ffmpeg" phraze in description
    for proc in psutil.process_iter():
      if proc.name() == "ffmpeg":
        os.kill(proc.pid, signal.SIGKILL)

    # Run new process
    time.sleep(1)
    subprocess.run(prep_process)

    # Prepared process gets transformed into Running process, the Running process gets now activated
    running_process = prep_process

  # If no movement sensor changes -> no layout changes
  elif prep_process == running_process:
    print('No changes')

  sum = 0
  