# MicrophoneSpectrumAnalyser
Takes in audio data from microphone and plots it. It's also supposed to plot the real-time discrete frequency domain representation of the input data (Plot present frequencies in audio data, (near) real-time).
This project is really just for myself, hosted on GitHub for easy access and reviews from more experienced users. It's my little project where I experiment with audio data and try to use the discrete fourier transform correctly (still working on that one and wrapping my head around how it works).

## Dependencies
Tested on Python 3.8.6
[numpy](https://pypi.org/project/numpy/)
[matplotlib](https://pypi.org/project/matplotlib/)
[sounddevice](https://pypi.org/project/sounddevice/)

Note: Numpy might throw a RuntimeError on Windows 10 [due to a bug](https://developercommunity.visualstudio.com/content/problem/1207405/fmod-after-an-update-to-windows-2004-is-causing-a.html#:~:text=My%20current%20expectation%20is%20that%20this%20will%20be%20able%20to%20be%20released%20near%20the%20end%20of%20January%202021.), so you'll need version 1.19.3 of numpy as of 10th December 2020. Expected fix is late January 2021.

## Code heavily inspired/copied from videos and online code-snippets:
[FluidicColours - NumPy Tutorials : 011 : Fast Fourier Transforms - FFT and IFFT](https://www.youtube.com/watch?v=su9YSmwZmPg&t=511s&ab_channel=FluidicColours)
[python-sounddevice documentation - Examples](https://python-sounddevice.readthedocs.io/en/0.3.14/examples.html#plot-microphone-signal-s-in-real-time)
[SimonXu - Discrete Fourier Transform - Simple Step by Step](https://www.youtube.com/watch?v=mkGsMWi_j4Q&t=508s&ab_channel=SimonXu)
