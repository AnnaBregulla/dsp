![Alt text](https://github.com/AnnaBregulla/dsp/blob/IIR-Assignment/guitar.jpg)
![Alt text](https://github.com/AnnaBregulla/dsp/blob/IIR-Assignment/set-up.jpg)
# IIR Assignment
Measure the stroke frequency of a guitar player by using the RGB light sensor of a laptop.
## Prerequisites
pip install opencv-contrib-py
pip install  opencv-python
pip intall nanotime
## Classes
### realtime_iir_main.py
By running this class a demonstration of a real-time measurement of the stroke frequency of a guitar player can be seen.
### iir2filter.py
With help of this class an iir filter of 2nd order can be implemented.
The handed over parameters for the constrctor contain the coefficients for creating an iir filter. "a0" should always be 1.
### iirfilter.py
With this class an array of 2nd order iir filters can be created. The usage of this class saves much code / time if real-time data should be filtered through several 2nd order filteres. The handed over parameter is and "sos" array that consist of several coefficients for creating several iir filters.
### webcam2rgb.py
see: https://github.com/berndporr/webcam2rgb/blob/main/webcam2rgb.py
