#!/usr/bin/env python
from __future__ import print_function
"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
from pdb import set_trace as br
import numpy as np
from collections import deque
import cv2
import time

def record_audio():
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	RECORD_SECONDS = 25
	WAVE_OUTPUT_FILENAME = "apt.wav"
	
	class meta_state:
		def __init__(self,history_length,target,tol):
			self.cap = cv2.VideoCapture(1)
			self.cap.set(cv2.CAP_PROP_CONTRAST, 5) 
			self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, -1)
			self.cap.set(cv2.CAP_PROP_EXPOSURE,-50) 
			self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 20) 
			self.num=0
			self.state_list=deque([])
			self.target_frequency=target
			self.len=history_length
			self.tolerance=tol
			for _ in range(0,history_length):
				self.state_list.append(False)	
		def push(self,freq):
			if 730 <= freq <= 760:
				self.state_list.append(True)
			else:
				self.state_list.append(False)
			self.state_list.popleft()
			if self.state_list[-1]==False and self.state_list[-1]!=self.state_list[-2]:
				for i in range(1,len(self.state_list)):
					if self.state_list[-i-1]==self.state_list[-1]:
						break
					else:
						#if the first element is not equal to any of the other elements
						# in the list and the first element is false (not lifting), we
						# have just transitioned from lifting to not lifting. Take a picture.
						# State must be: [false,true,true,true,true,...]
						if i==len(self.state_list)-1:
							time.sleep(.15)
							print("Taking a picture")
							ret, frame = self.cap.read()
							if ret:
								cv2.imwrite("test_"+str(self.num)+".jpg",frame)
								self.num+=1
							del ret,frame

	ms=meta_state(10,746,100)
	p = pyaudio.PyAudio()
	SWIDTH=p.get_sample_size(FORMAT)
	WINDOW = np.blackman(CHUNK)
	
	#For live streaming:
	stream = p.open(format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				input=True,
				frames_per_buffer=CHUNK,
				input_device_index = 0)
	print("Listening like a spider on in a web...")
	
	## For streaming from wav file:
	# f = wave.open('lift.wav')
	# FORMAT=p.get_format_from_width(f.getsampwidth())
	# CHANNELS=f.getnchannels()
	# RATE=f.getframerate()
	# print("FORMAT: "+str(FORMAT)+"\nCHANNELS: "+str(CHANNELS)+"\nRATE: "+str(RATE))
	# stream = p.open(format=FORMAT,
	# 			channels=CHANNELS,
	# 			rate=RATE,
	# 			output=True)
	# data=f.readframes(CHUNK)
	# print("Processing file...")
	
	thefreq=0
	frames = []
	
	# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		# while data != '':
	while True:
		data = stream.read(CHUNK,exception_on_overflow = False)
		# data=f.readframes(CHUNK)
		# stream.write(data)
		
		indata = np.array(wave.struct.unpack("%dh"%(len(data)/SWIDTH),data))*WINDOW
		# Take the fft and square each value
		fftData=abs(np.fft.rfft(indata)**2)
		# find the maximum
		maxi = fftData[1:].argmax() + 1
		# use quadratic interpolation around the max
		if maxi != len(fftData)-1:
			y0,y1,y2 = np.log(fftData[maxi-1:maxi+2:])
			x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
			# find the frequency and output it
			thefreq = (maxi+x1)*RATE/CHUNK
			# print("The freq is %f Hz." % (thefreq))
		else:
			thefreq = maxi*RATE/CHUNK
			# print("The freq is %f Hz." % (thefreq))
		ms.push(thefreq)
		# print(ms.state_list)
		# frames.append(data)

	print("* done\n") 

	stream.stop_stream()
	stream.close()
	p.terminate()
	#uncomment below and frames.append above to save audio
	# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	# wf.setnchannels(CHANNELS)
	# wf.setsampwidth(p.get_sample_size(FORMAT))
	# wf.setframerate(RATE)
	# wf.writeframes(b''.join(frames))
	# wf.close()
record_audio()
