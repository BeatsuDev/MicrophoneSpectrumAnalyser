import time
import queue

import sounddevice as sd
import numpy as np

from numpy.fft import fft, fftfreq

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

ax[1].set_xlim(50, 2500)
ax[1].set_ylim(0, 0.04)


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

	# Ensure equal length samples
	wait_for_length = 500

	while 1:
		try:
			channel_left = audio_data_left.get_nowait()
			# channel_right = audio_data_right.get_nowait()
		except:
			if not len(data_left) > wait_for_length: continue
			break

		data_left = [*data_left, *channel_left]
		# data_right = [*data_left, *channel_right]


	plotdata[0] = [*plotdata[0], *data_left] 
	# plotdata[1] = [*plotdata[1], *data_right]

	plotdata[0] = plotdata[0][-44100*duration//downsampling:]
	# plotdata[1] = plotdata[1][-44100*duration:]

	#
	# FREQUENCY CALCULATION
	#

	n = len(data_left)

	time_delta = n/44100


	freqs = fftfreq(n)
	mask = freqs > 0
	fft_vals = fft(data_left)
	fft_theo = 2.0*np.abs(fft_vals/n)

	"""

	# Keep half the frequency bins because of the Nyquist limit
	left_freq = left_freq[:len(left_freq)//2]

	# Get magnitude of every complex value frequency bin
	left_freq = list(map( lambda n: np.sqrt(n.real**2 + n.imag**2) , left_freq))

	# Double every value because of the two sided frequency plot from fourier transform
	left_freq *= 2
	"""

	# Not quite sure if this is correct, but it somehow works in exactly this case... 
	x = freqs[mask] * 44100 / (1/(time_delta*20))
	y = fft_theo[mask]

	print(time_delta*2)

	line_freq_left.set_data(x, y)
	# line_freq_right.set_data(freq_range, right_freq)

	line_left.set_data(range(len(plotdata[0])), plotdata[0])
	# line_right.set_data(range(len(plotdata[1])), plotdata[1])



stream = sd.InputStream(
	samplerate = 44100,
	channels = 2,
	callback = audio_callback
)


plotdata = [np.zeros(int( 44100 * duration))] *2

ani = animation.FuncAnimation(fig, plot_update, interval=10)

with stream:
	plt.show()