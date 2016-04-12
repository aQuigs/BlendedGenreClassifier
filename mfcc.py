#!/usr/bin/python

import sys, os, glob, numpy
wd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(wd + '/python_speech_features')
from features import mfcc
import scipy.io.wavfile as wav

DIR = '/home/quiggles/Desktop/513music/single-genre'
OUTDIR = wd + '/songdata'


def getMFCC(filename):
    (rate,sig) = wav.read(filename)
    mfcc_feat = mfcc(sig,rate)
    l = len(mfcc_feat)/4
    quartileMean1 = numpy.mean(mfcc_feat[:l],      axis=0)
    quartileMean2 = numpy.mean(mfcc_feat[l:2*l],   axis=0)
    quartileMean3 = numpy.mean(mfcc_feat[2*l:3*l], axis=0)
    quartileMean4 = numpy.mean(mfcc_feat[3*l:],    axis=0)

    return numpy.concatenate([quartileMean1, quartileMean2, quartileMean3, quartileMean4])

def writeMFCC(filename, outdir):
    a = getMFCC(filename)
    with open(outdir + '/' + os.path.splitext(os.path.basename(filename))[0] + ".csv", 'w') as f:
        addComma = False
        for val in a:
            if addComma:
                f.write(',')
            f.write(str(val))
            addComma = True
        f.write('\n')
    

def generateMFCCData(indir, outdir):
    for f in glob.glob(outdir + '/*.csv'):
        os.remove(f)

    for f in glob.glob(indir + '/*.wav'):
        try:
            writeMFCC(f, outdir)
            newfilename = os.path.splitext(os.path.basename(f))[0]
            print('YES: '+ newfilename)
            if 'classify-me' not in indir:
                os.rename(f, indir+"/classify-me/" + newfilename+".wav")
                os.rename(indir+'/' + newfilename + ".mp3", indir+"/classify-me/" + newfilename+".mp3")
        except:
            print('NO: '+f)

if __name__ == '__main__':
    generateMFCCData(DIR, OUTDIR)
