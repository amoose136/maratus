#!/usr/bin/env python
from __future__ import print_function
"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
from pdb import set_trace as br
import numpy as np

def record_audio():
	CHUNK = 2048
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	RECORD_SECONDS = 25
	WAVE_OUTPUT_FILENAME = "apt.wav"
	p = pyaudio.PyAudio()
	SWIDTH=p.get_sample_size(FORMAT)
	WINDOW = np.blackman(CHUNK)
	#open a wav format music
	f = wave.open('lift.wav')
	# stream = p.open(format=FORMAT,
	# 			channels=CHANNELS,
	# 			rate=RATE,
	# 			input=True,
	# 			frames_per_buffer=CHUNK,
	# 			input_device_index = 0)
	FORMAT=p.get_format_from_width(f.getsampwidth())
	CHANNELS=f.getnchannels()
	RATE=f.getframerate()
	print("FORMAT: "+str(FORMAT)+"\nCHANNELS: "+str(CHANNELS)+"\nRATE: "+str(RATE))
	stream = p.open(format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				output=True)
	print("* Recording audio...")
	frames = []
	data=f.readframes(CHUNK)
	# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	while data != '':
		# data = stream.read(CHUNK)
		data=f.readframes(CHUNK)
		stream.write(data)
		
		indata = np.array(wave.struct.unpack("%dh"%(len(data)/SWIDTH),data))*WINDOW
		# Take the fft and square each value
		fftData=abs(np.fft.rfft(indata)**2)
		# find the maximum
		which = fftData[1:].argmax() + 1
		# use quadratic interpolation around the max
		if which != len(fftData)-1:
			y0,y1,y2 = np.log(fftData[which-1:which+2:])
			x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
			# find the frequency and output it
			thefreq = (which+x1)*RATE/CHUNK
			print("The freq is %f Hz." % (thefreq))
		else:
			thefreq = which*RATE/CHUNK
			print("The freq is %f Hz." % (thefreq))
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
