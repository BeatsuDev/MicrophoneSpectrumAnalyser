import time
import queue

import sounddevice as sd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

audio_data_left = queue.Queue()
audio_data_right = queue.Queue()

fig, ax = plt.subplots(2, 1)

duration = 1
downsampling = 3

line_left, = ax[0].plot([],[])
line_freq_left, = ax[1].plot([], [])

ax[0].set_xlim(0, 44100//downsampling)
ax[0].set_ylim(-.8, .8)

ax[1].set_xlim(200, 1200)
ax[1].set_ylim(0, 15)



def add_at_frequency_interval(sound_data, frequency, samplerate=44100, rotation_step=1):

	offsets = []
	for i in range(frequency):
		offsets.append(np.abs((1 + sum(sound_data[i*rotation_step::(samplerate//frequency)]))**2))
		if i*rotation_step > frequency//2: break

	return max(offsets)


def audio_callback(indata: np.ndarray, frames: int, time, status):
	global downsampling
	left_data = []
	# right_data = []

	for left, right in indata:
		left_data.append(left)
		# right_data.append(right)

	# Downsample
	left_data = left_data[::downsampling]
	# right_data = right_data[::downsampling]

	audio_data_left.put(np.array(left_data))
	# audio_data_right.put(np.array(right_data))
	


def plot_update(*args):
	global duration, plotdata

	data_left = []
	# data_right = []

	while 1:
		try:
			channel_left = audio_data_left.get_nowait()
			# channel_right = audio_data_right.get_nowait()
		except:
			break

		data_left = [*data_left, *channel_left]
		# data_right = [*data_left, *channel_right]

	plotdata[0] = [*plotdata[0], *data_left] 
	# plotdata[1] = [*plotdata[1], *data_right]

	plotdata[0] = plotdata[0][-44100*duration//downsampling:]
	# plotdata[1] = plotdata[1][-44100*duration:]

	freq_range = np.arange(200, 1200+1, 10)

	left_freq = []
	highest = []
	# right_freq = []
	for freq in freq_range:
		left_freq.append( add_at_frequency_interval(plotdata[0][-44100:], freq, rotation_step=20) )
		# right_freq.append( add_at_frequency_interval(plotdata[1][-44100:], freq) )

		if left_freq[-1] > 7:
			highest.append(freq)

	line_freq_left.set_data(freq_range, left_freq)
	# line_freq_right.set_data(freq_range, right_freq)

	line_left.set_data(range(len(plotdata[0])), plotdata[0])
	# line_right.set_data(range(len(plotdata[1])), plotdata[1])

	print(f"{highest}\t\t\t\t\t", end='\r')



stream = sd.InputStream(
	samplerate = 44100,
	channels = 2,
	callback = audio_callback
)


plotdata = [np.zeros(int( 44100 * duration))] *2

ani = animation.FuncAnimation(fig, plot_update, interval=10)

with stream:
	plt.show()