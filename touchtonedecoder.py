# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 11:08:45 2020

@author: bregu
"""

import numpy as np
import voice_enhancer as ve
#import matplotlib.pyplot as plt

class MyNrDetectionClass:
    # Constructors:
    def __init__(self, audio_data):
        self.audio_data = audio_data
        self.treshold = -200 # dB
        self.frequencies = [697, 770, 852, 941, 1209, 1336, 1477] # Hz
        self.aliasingF = self.getAliasingFrequencies(audio_data.sample_rate, self.frequencies) # [303, 230, 148, 59, 209, 336, 477]      
        
    # Methods:
    def getAliasingFrequencies(self, sample_rate, signal_frequencies): 
        aliasingF = []    
        for i in range(len(signal_frequencies)):
            N = round(signal_frequencies[i] / sample_rate)
            aliasingF.append(abs(signal_frequencies[i] - N * sample_rate))   
        return aliasingF
    
    def detectNumbersFromAudioData(self):
        f_counter = np.zeros(len(self.aliasingF)) # counts if aliasing f are in samples: eg [0 1 0 0 0 1 0] means 230 Hz (770 Hz) and 336 Hz (1336 Hz) are in sample data
        f_start, f_end = self.cleaned_fStart_fEnd() # f_start and f_end frequencies define detected aliasing frequencies in sample data
        for i in range(len(f_start)):
            for j in range(len(self.aliasingF)):
                if (self.aliasingF[j] > f_start[i]) and (self.aliasingF[j] < f_end[i]):
                    f_counter[j] = f_counter[j] + 1 
        
        f = [] # saves detected possible frequencies
        for i in range(len(f_counter)):
           if f_counter[i] > 0:
               f.append(self.frequencies[i]) # eg f = [697, 941, 1336] -> Nr 0 & 2
             
        detectedNr = []
        for i in range(10): # every round detection if number i is in sample
            fOfNr = self.returnFrequenciesOfNumber(i) # eg [697, 1336] corresponds to 2
            counter = 0
            for j in range(len(f)): # eg f = [697, 941, 1336]
                for k in range(len(fOfNr)): # eg [697, 1336] 
                    if(f[j] == fOfNr[k]):
                        counter = counter + 1
                        if (counter == 2): # if 2 frequencies within 'f' and 'fOfNr' match eachother number that corresponds to 'fOfNr' is in sample
                            detectedNr.append(i)    
        return detectedNr

    def detectOneDigitFromChunkOfRecording(self, number_toDetect):
        numberInRecord = False
        frequenciesOfNr = self.returnFrequenciesOfNumber(number_toDetect) 
        f_counter = self.f_counter() # counts if frequencies from above could be in data 
        f = [] # saves detected possible frequencies
        for i in range(len(f_counter)):
           if f_counter[i] > 0:
               f.append(self.frequencies[i])  
        counter = 0
        for i in range(len(frequenciesOfNr)): # if frequencies of number matches detected f, digit should be in recording 
            for j in range(len(f)):
                if frequenciesOfNr[i] == f[j]:
                    counter = counter + 1
        if counter >= 2:
            numberInRecord = True
        
        return numberInRecord
   
    def returnFrequenciesOfNumber(self, numer_toDetect):
       if numer_toDetect == 0:
           return [941, 1336]
       
       if numer_toDetect == 1:
           return [697, 1209]
       
       if numer_toDetect == 2:
           return [697, 1336]
       
       if numer_toDetect == 3:
           return [697, 1477]
       
       if numer_toDetect == 4:
           return [770, 1209]
       
       if numer_toDetect == 5:
           return [770, 1336]
       
       if numer_toDetect == 6:
           return [770, 1477]
       
       if numer_toDetect == 7:
           return [852, 1209]
       
       if numer_toDetect == 8:
           return [852, 1336]
       
       if numer_toDetect == 9:
           return [852, 1477]
       
    def f_counter(self): # counts if frequencies from above could be in data 
        f_counter = np.zeros(len(self.frequencies)) 
        f_start, f_end = self.cleaned_fStart_fEnd() 
        for i in range(len(self.frequencies)):
            for j in range(1,11): # division till 10
                for k in range(len(f_start)):
                    if (self.frequencies[i]/j > f_start[k]) and (self.frequencies[i]/j < f_end[k]):
                        f_counter[i] = f_counter[i] + 1 
        return f_counter
    
 
    def f_inData(self):
        filtered_data = self.filterDataForNrDetection() # returns audio data which was set to 0 if below treshold value
        f_inData = [] # saves remaining frequencies from audio data after being filtered 
        for i in range(int(len(filtered_data)/2)): # due to no mirror -> /2
            if filtered_data[i] != 0:
                f = i * self.audio_data.sample_rate / self.audio_data.nr_samples
                f_inData.append(f)
        return f_inData
    
    def filterDataForNrDetection(self):
        f_filtered = np.zeros(self.audio_data.nr_samples)
        for i in range(self.audio_data.nr_samples):
            if self.audio_data.audio_data_fft_abs_dB[i] > self.treshold:
                 f_filtered[i] = self.audio_data.audio_data_fft_abs[i]
        #plt.plot(f_filtered)
        #plt.axis([1250, 2000, 0, 50000]) 
        #plt.show()
        return f_filtered      
        
    def f_start_end(self):
        f_start = []  
        f_end = []
        f_inData = self.f_inData()
        for i in range(len(f_inData)-1):
            if ((f_inData[i+1]-f_inData[i]) > 2): # difference of greater than 2 is hint for starting/ending frequencies which indicate a frequency that may occur
                if(f_inData[i+1] != 0):
                    f_start.append(f_inData[i+1])
                if(f_inData[i] != 0):   
                    f_end.append(f_inData[i])
        f_end.append(f_inData[len(f_inData)-1])   
        return f_start, f_end
    
    def cleaned_fStart_fEnd(self):
        f_start, f_end = self.f_start_end()
        f_start_new = []
        f_end_new = []
        for i in range(len(f_start)): # clean data from frequencies below 10 Hz
            if f_start[i] > 10:
                f_start_new.append(f_start[i])
        for j in range(len(f_end)):
            if f_end[j] > 10:
                f_end_new.append(f_end[j])
                
        return f_start_new, f_end_new
   
       
# main:    
#### 5 ####
file_type_tel = '.dat'
# detect numbers 0...9 from touch tone telephone
for i in range(1,10):
    file_name_tel = 'ugrad_matric_' + str(i) + '.dat'
    AudioData_tel = ve.MyAudioProcessingClass_WAV(file_name_tel, file_type_tel)      

    # plot wav-file in time domain
    #AudioData_tel.plotAudioDataInTimeDomain()

    # plot wav-file in frequency domain
    #AudioData_tel.plotAudioDataInFrequencyDomain_noLog()
    #AudioData_tel.plotAudioDataInFrequencyDomain_Log()
    
    #### a/b ####
    NrDet = MyNrDetectionClass(AudioData_tel)
    nr_detected = NrDet.detectNumbersFromAudioData()
    print(f"ugrad_matric_{i}.dat: detected numbers: {nr_detected}")