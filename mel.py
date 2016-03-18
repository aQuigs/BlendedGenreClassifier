from example import example
import os

#you need the following libraries as well as base.py, sigproc.py in the features folder
#scipy
#numpy
basedirectoryofmusic = '/home/quiggles/BlendedGenreClassifier/cse513/music/'
directoryforprocessedcsv = '/home/quiggles/BlendedGenreClassifier/cse513/musicstuff/'

for filename in os.listdir(basedirectoryofmusic):
    example(filename, basedirectoryofmusic + filename, directoryforprocessedcsv)