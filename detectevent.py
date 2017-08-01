#!/usr/bin/env python
from __future__ import print_function
"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
from pdb import set_trace as br

def record_audio():
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = 5
	WAVE_OUTPUT_FILENAME = "apt.wav"

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

	print("* Recording audio...")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	print("* done\n") 

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
br()
