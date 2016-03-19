#!/usr/bin/python

import sys, os, glob, string
wd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(wd + '/pytagger-0.5')
sys.path.append(wd + '/pytagger-0.5/tagger')
from tagger import ID3v2
from mfcc import generateMFCCData
from genreManager import writeGenresToDisk

DIR = '/home/quiggles/Desktop/513music/single-genre/classify-me'
OUTDIR = wd + '/songdata'

if __name__ == '__main__':
    writeGenresToDisk(DIR, OUTDIR)
    generateMFCCData(DIR, OUTDIR)

