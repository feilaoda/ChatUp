#!/usr/bin/env python
import sys
import wave
import wave


# from pylab import *
def show_wave_n_spec(speech):
    spf = wave.open(speech,'r')
    sound_info = spf.readframes(-1)
    sound_info = fromstring(sound_info, 'Int16')
    f = spf.getframerate()
    
    subplot(211)
    plot(sound_info)
    title('Wave from and spectrogram of %s' % sys.argv[1])

    subplot(212)
    spectrogram = specgram(sound_info, Fs = f, scale_by_freq=True,sides='default')
    
    show()
    spf.close()

# fil = sys.argv[1]

# show_wave_n_spec(fil)


w = wave.open('test.wav', 'r')
for i in range(w.getnframes()):
    frame = w.readframes(i)

    all_zero = True
    for j in range(len(frame)):
        # check if amplitude is greater than 0
        if ord(frame[j]) > 0:
            all_zero = False
            break

    if all_zero:
        # perform your cut here
        print 'silence found at frame %s' % w.tell()
