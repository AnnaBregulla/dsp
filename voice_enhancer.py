# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:33:03 2020

@author: bregu
"""
import scipy.io.wavfile as scipy
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wavfile

class MyAudioProcessingClass_WAV:
    # static class instace
    nr_figures = 1
    
    # Constructors:
    def __init__(self, file_name, file_type):
        self.file_name = file_name
        if file_type == '.wav':
            self.sample_rate, self.audio_data =  scipy.read(file_name) # load wav file
        if file_type == '.dat':
            data = np.loadtxt(file_name) # load dat file
            self.audio_data = data[:,1]
            self.sample_rate = 1000 # Hz
        
        self.audio_data_fft = np.fft.fft(self.audio_data)   
        self.audio_data_fft_abs = abs(self.audio_data_fft)   
        self.audio_data_fft_abs_dB = 20 * np.log(self.audio_data_fft_abs/np.max(self.audio_data_fft_abs))
        self.nr_samples = len(self.audio_data)
        self.length_audio = self.nr_samples / self.sample_rate # s
        
    # Methods:  
    def plotAudioDataInTimeDomain(self):
        time = np.linspace(0, self.length_audio, self.nr_samples)
        plt.figure(self.nr_figures)
        self.nr_figures = self.nr_figures + 1 
        plt.plot(time, self.audio_data, label = "audio data\nsample rate: " + str(self.sample_rate) + " Hz") 
        plt.title('Audio Data ("' + self.file_name + '")\nTime Domain' )
        plt.legend()
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude") 
        plt.grid(True)
        plt.savefig('AudioDataInTimeDomain.svg')
        plt.show()
        
        
    def plotAudioDataInFrequencyDomain_noLog(self):
        plt.figure(self.nr_figures)
        self.nr_figures = self.nr_figures + 1 
        plt.plot(np.linspace(0, self.sample_rate, self.nr_samples), self.audio_data_fft_abs, label = "audio data\nf domain - mirror, no log axis\nsample rate: " + str(self.sample_rate) + " Hz") 
        #plt.plot(np.linspace(0, int(self.sample_rate/2), int(self.nr_samples/2)), self.audio_data_fft_abs[0:(int(self.nr_samples/2))], label = "audio data\nf domain - no mirror, no log axis\nsample rate: " + str(self.sample_rate) + " Hz") 
        plt.title('Audio Data ("' + self.file_name + '")\nFrequency Domain')
        plt.legend()
        plt.xlabel("Frequence [Hz]")
        plt.ylabel("Amplitude")
        #plt.axis([0, 2000, 0, 2E6]) 
        plt.grid(True)
        plt.show()
                     
    def plotAudioDataInFrequencyDomain_Log(self):
        plt.figure(self.nr_figures)
        self.nr_figures = self.nr_figures + 1 
        plt.plot(np.linspace(0, self.sample_rate, self.nr_samples), self.audio_data_fft_abs_dB, label = "audio data\nf domain - mirror, log axis\nsample rate: " + str(self.sample_rate) + " Hz") 
        #plt.plot(np.linspace(0, int(self.sample_rate/2), int(self.nr_samples/2)), self.audio_data_fft_abs_dB[0:int(self.nr_samples/2)], label = "audio data\nf domain - no mirror, log axis\nsample rate: " + str(self.sample_rate) + " Hz") 
        plt.legend()
        plt.title('Audio Data ("' + self.file_name + '")\nFrequency Domain')
        plt.xlabel("Frequence [Hz]")
        plt.xscale('log')
        plt.ylabel("Amplitude [dB]")
        plt.grid(True)
        plt.savefig('AudioDataInFrequenceDomain.svg')
        plt.show()
        
    def improveQualityOfVoice(self, lowerUpper_limits, multipl_factor):
        normalized_audio_data_fft = self.audio_data_fft / max(self.audio_data_fft)
        filtered_audio_data_fft = normalized_audio_data_fft 
        k = np.zeros((2, len(lowerUpper_limits[0])), dtype = int)
        
        for i in range(len(lowerUpper_limits[0])):
            k[0,i] = int(self.nr_samples / self.sample_rate * lowerUpper_limits[0,i])
            k[1,i] = int(self.nr_samples / self.sample_rate * lowerUpper_limits[1,i])
            
            filtered_audio_data_fft[k[0,i]:k[1,i]+1] = normalized_audio_data_fft[k[0,i]:k[1,i]+1] * multipl_factor
            filtered_audio_data_fft[self.nr_samples-k[1,i]:self.nr_samples-k[0,i]+1] = normalized_audio_data_fft[self.nr_samples-k[1,i]:self.nr_samples-k[0,i]+1] * multipl_factor
       
        #plt.plot(abs(filtered_audio_data_fft))
        #plt.show()
        filtered_audio_data_ifft = np.fft.ifft(filtered_audio_data_fft)
        normalized_filtered_audio_data_ifft = filtered_audio_data_ifft / max(filtered_audio_data_ifft)
        filtered_audio_data_ifft = normalized_filtered_audio_data_ifft * 32767 
        filtered_audio_data = np.around(filtered_audio_data_ifft).real.astype(np.int16)
        return filtered_audio_data
    
    def plotDataImprovedVoice(self, audio_data):
        plt.figure(self.nr_figures)
        self.nr_figures = self.nr_figures + 1 
        time = np.linspace(0, self.length_audio, self.nr_samples) 
        plt.plot(time, audio_data, label = "improved audio data\nsample rate: " + str(self.sample_rate) + " Hz")
        plt.title('Audio Data ("' + self.file_name + '") - Time Domain')
        plt.legend()
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude") 
        plt.grid(True)
        plt.show()
        
        
# main:
file_name = 'original.wav'
file_type = '.wav'

#### 2 ####
AudioData = MyAudioProcessingClass_WAV(file_name, file_type)

# plot wav-file in time domain
AudioData.plotAudioDataInTimeDomain()

# plot wav-file in frequency domain
AudioData.plotAudioDataInFrequencyDomain_noLog()
AudioData.plotAudioDataInFrequencyDomain_Log()

#### 4 ####
# improve quality of voice 
lowerUpper_limits = np.array([[175, 6000], [500, 10000]]) # Hz
multipl_factor = 2
filtered_audio_data = AudioData.improveQualityOfVoice(lowerUpper_limits, multipl_factor)
AudioData.plotDataImprovedVoice(filtered_audio_data)
wavfile.write('improved.wav', AudioData.sample_rate, filtered_audio_data)             
    