"""
Author: Lorenzo

Date: 1 May, 2023

This script generates a dict where keys are notes and values are frequencies.
Then it takes a list of note representing the melody, a list of note representing harmony and it generates a wave file PCM-16 bit. 

Note: don't struggle with the built-in module "wave". Use scipy!
"""
import numpy as np
from  scipy.io import wavfile
import matplotlib.pyplot as plt


######################################## INPUTS ########################################
#
#
melody_notes_list = ['do4', 'do4', 'do4', 'do5','fa4','fa4','fa4','fa3','do4','do4','do4','sol4','do5','do5','do5'] # melody
harmony_notes_list = ['do4', 'sol4'] # harmony
tone_duration = 1 # seconds
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
    'la0': f_do1 //(g**3),
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
# composer melody
#
t = np.linspace(0, tone_duration, fs * tone_duration, endpoint=False)

# left channel
track_melody_L = np.array([])
for note in melody_notes_list:
    f = frequencies[note]
    track_melody_L = np.append( track_melody_L, np.sin(2 * pi * f * t) )

# right channel
track_melody_R = np.array([])
for note in melody_notes_list:
    f = frequencies[note]
    track_melody_R = np.append( track_melody_R, np.sin(2 * pi * f * t) )


#
# composer harmony
#
t = np.linspace(0, len(track_melody_L) // fs, len(track_melody_L), endpoint=False)

# left channel
track_harmony_L = np.zeros(len(t))
for note in harmony_notes_list:
    f = frequencies[note]
    track_harmony_L += np.sin(2 * pi * f * t)

# right channel
track_harmony_R = np.zeros(len(t))
for note in harmony_notes_list:
    f = frequencies[note]
    track_harmony_R += np.sin(2 * pi * f * t)

# normalize and convert into int
amplitude = 2 ** (depth - 1) - 10 # to account the sign and avoid distorsion
mixed_track_L =  track_melody_L + track_harmony_L
mixed_track_R = track_melody_R + track_harmony_L
norm_track_L = (mixed_track_L / mixed_track_L.max()) * amplitude
norm_track_R = (mixed_track_R / mixed_track_R.max()) * amplitude
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
# dft = np.fft.fft(track_harmony_L)
# freq = np.fft.fftfreq(n, 1 / fs)
# plt.plot(freq, np.abs(dft.real))
# plt.xlabel('f [Hz]')
# plt.ylabel('Amplitude')
# plt.show()


#
# write the wav file
#
audio = np.vstack((audio_L, audio_R)).T
wavfile.write('song.wav', fs, audio)