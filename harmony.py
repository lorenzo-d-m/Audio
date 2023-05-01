"""
Author: Lorenzo

Date: 1 May, 2023

This script generates a dict where keys are notes and values are frequencies.
Then it takes a list of note representing the harmony and it generates a wave file PCM-16 bit. 

Note: don't struggle with the built-in module "wave". Use scipy!
"""
import numpy as np
from  scipy.io import wavfile
import matplotlib.pyplot as plt


######################################## INPUTS ########################################
#
#
notes_list = ['do4', 'mi4', 'sol4'] # harmony
duration = int(12) # seconds
########################################### # ###########################################

#
# params
#
pi = np.pi
fs = int(44100) # Hz
depth = int(16) # if depth is 16, scipy.io.wavfile wants np.int16 values --> PCM 16 bits
# ref: https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html


#
# dict generation of notes and frequencies 
# frequencies creation by multipling the 440 Hz by 1.059463
#
notes_name = ['do', 'do#', 're', 're#', 'mi', 'fa', 'fa#', 'sol', 'sol#', 'la', 'la#', 'si']
g = 2 ** (1 / 12) # temperate scale: the 12th root of 2 is 1.059463. Then 1.059463^12 = 2, that is an octave
f_do1 = 440 // (1.059463 ** 45) #45 are the notes between la4 and do1

# freq bellow do1
frequencies = {
    'la0': f_do1 // (g**3),
    'la#0': f_do1 // (g**2),
    'si0': f_do1 // g,
}
# freq above do1
i = 0
for note_num in range(1,9):
    for note_name in notes_name:
        frequencies[f'{note_name}{note_num}'] = f_do1 * (g ** i)
        i += 1


#
# note and frequencies creaton by doubling and halving the dodecaphone reference frequencies
# no differences are heard with respect to the used generation mode
#
# notes_name = ['la4', 'la#4', 'si4', 'do5', 'do#5', 're5', 're#5', 'mi5', 'fa5', 'fa#5', 'sol5', 'sol#5']
# g = 2 ** (1 / 12) # temperate scale: the 12th root of 2 is 1.059463. Then 1.059463^12 = 2, that is an octave

# frequencies = dict()
# for i, note_name in enumerate(notes_name):
#     frequencies[note_name] = int( 440 * (g ** i) )

# for j in range(4):
#     for i, note_name in enumerate(notes_name):
#         note = note_name[0:-1]
#         p = int(note_name[-1])
#         frequencies[f'{note}{p+j+1}'] = int( frequencies[f'{note}{p+j}'] * 2 )

# for j in range(4):
#     for i, note_name in enumerate(notes_name):
#         note = note_name[0:-1]
#         p = int(note_name[-1])
#         frequencies[f'{note}{p-j-1}'] = int( frequencies[f'{note}{p-j}'] / 2 )


#
# composer
#
t = np.linspace(0, duration, fs * duration, endpoint=False)

# left channel
track_L = np.zeros(len(t))
for note in notes_list:
    f = frequencies[note]
    track_L += np.sin(2 * pi * f * t)

# right channel
track_R = np.zeros(len(t))
for note in notes_list:
    f = frequencies[note]
    track_R += np.sin(2 * pi * f * t)

# normalize and convert into np.int16
amplitude = 2 ** (depth - 1) - 10 # to account the sign and avoid distorsion
norm_track_L = (track_L / track_L.max()) * amplitude
norm_track_R = (track_R / track_R.max()) * amplitude
audio_L = norm_track_L.astype(np.int16)
audio_R = norm_track_R.astype(np.int16)


#
# time view
#
# time = np.linspace(0, len(audio_L) / fs, len(audio_L), endpoint=False)
# plt.plot(time,audio_L)
# plt.xlabel('t [s]')
# plt.ylabel('Amplitude')
# plt.show()


#
# frequency view
#
# n = len(t)
# dft = np.fft.fft(norm_track_L)
# freq = np.fft.fftfreq(n, 1 / fs)
# plt.plot(freq, np.abs(dft.real))
# plt.xlabel('f [Hz]')
# plt.ylabel('Amplitude')
# plt.show()


#
# write the wav file
#
audio = np.vstack((audio_L, audio_R)).T
wavfile.write('harmony.wav', fs, audio)