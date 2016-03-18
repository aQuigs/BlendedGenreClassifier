from example import example
import os

#you need the following libraries as well as base.py, sigproc.py in the features folder
#scipy
#numpy
basedirectoryofmusic = 'C:/Users/Mel/Desktop/cse513/music/'
directoryforprocessedcsv = 'C:/Users/Mel/Desktop/cse513/musicstuff/'

for filename in os.listdir(basedirectoryofmusic):
    example(filename, basedirectoryofmusic + filename, directoryforprocessedcsv)