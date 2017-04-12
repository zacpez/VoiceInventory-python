# VoiceInventory-python
This is a low fidelity prototype for a voice activate workshop. Use speech to highlight tool locations around a shop. In this example Google Speech Recoginition was used, however there are more modules to try. 

Travis says: 
[![Build Status](https://travis-ci.org/zacpez/VoiceInventory-python.svg?branch=master)](https://travis-ci.org/pantsbuild/pants/branches).

#### Example screenshot when user says "pliers": ####

![Prototype positional output](https://github.com/zacpez/VoiceInventory-python/blob/master/inventory-sample.png?raw=true)

Voice Inventory was built on Debianx64 using python 3.4, so the basic install intructions are as follows:

### System Requirements ###
* ``apt-get install python3``
* ``apt-get install python-pyaudio python3-pyaudio``
* ``apt-get install python3-tk``

### Python modules ###
* ``pip install pyaudio``
* ``pip install Queue``
* ``pip install SpeechRecognition``
* ``pip install python-tk``

### Vocal test items: ###
Say any of the following words, and the program will locate it in the virtual tool bench.

 Voice  | Inventory | Commands 
| :--------------------------: | :---------------------------: | :------------------------------: |
| hammer | mallet | ax |
| saw | hacksaw | level|
| screwdriver | Phillips screwdriver | wrench |
| monkey wrench| pipe wrench | chisel |
| scraper | wire stripper | hand drill |
| vise | pliers | toolbox | 
| plane | electric drill | drill bit |
| circular saw | power saw | pipe |
| ander | router | wire |
| nail | washer | nut
| wood screw | machine screw | bolt | 



