#!/usr/bin/python

import sys, os, glob, string
wd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(wd + '/pytagger-0.5')
sys.path.append(wd + '/pytagger-0.5/tagger')
sys.path.append(wd + '/python_speech_features')
from tagger import ID3v2
from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav
import fileinput
import numpy

DIR = '/home/quiggles/Desktop/513music/single-genre/classify-me'
OUTDIR = wd + '/songdata'   

def writeGenre(filename, outdir):
    tag = ID3v2(filename)
    with open(outdir + '/' + os.path.basename(os.path.splitext(filename)[0]) + '.genre','w') as f:
        for frame in tag.frames:
            if frame.fid == 'TCON':
                f.write(frame.strings[0].split('\x00')[0]) # remove padding \x00
                return

def updateGenre(filename):
    tag = ID3v2(filename)
    for frame in tag.frames:
        if frame.fid == 'TCON':
            if len(string.strip(frame.strings[0])) != 0:
                return
            frame.strings[0] = string.strip(frame.strings[0])
            if frame.strings[0] == '(20)':
                frame.set_text('Alternative')
            elif frame.strings[0] == '(15)':
                frame.set_text('Rap')
            elif frame.strings[0] == '(79)':
                frame.set_text('Hard Rock')
            elif frame.strings[0] == '(121)':
                frame.set_text('Punk Rock')
            elif frame.strings[0] == '(13)':
                frame.set_text('Pop')
            elif frame.strings[0] == 'Rap Rock':
                frame.set_text('Rap Rock')
            tag.commit()
    print(str(i))

def listGenre(filename, masterdict):
    tag = ID3v2(filename)
    for frame in tag.frames:
        if frame.fid == 'TCON':
            genre = frame.strings[0].split('\x00')[0]
            if genre in masterdict:
                masterdict[genre] += 1
            else:
                masterdict[genre] = 0

def writeGenresToDisk():
    global DIR
    global OUTDIR
    for f in glob.glob(OUTDIR + '/*.genre'):
        os.remove(f)

    # masterdict = dict()
    for f in glob.glob(DIR + '/*.mp3'):
        writeGenre(f, OUTDIR)
        # updateGenre(f)
        # listGenre(f, masterdict)
    # print(str(masterdict))


def writeMFCC(filename, outdir):
    (rate,sig) = wav.read(filename)
    mfcc_feat = mfcc(sig,rate)
    l = len(mfcc_feat)/4
    quartileMean1 = numpy.mean(mfcc_feat[:l],      axis=0)
    quartileMean2 = numpy.mean(mfcc_feat[l:2*l],   axis=0)
    quartileMean3 = numpy.mean(mfcc_feat[2*l:3*l], axis=0)
    quartileMean4 = numpy.mean(mfcc_feat[3*l:],    axis=0)

    a = numpy.concatenate([quartileMean1, quartileMean2, quartileMean3, quartileMean4])
    with open(outdir + '/' + os.path.splitext(os.path.basename(filename))[0] + ".csv", 'w') as f:
        addComma = False
        for val in a:
            if addComma:
                f.write(',')
            f.write(str(val))
            addComma = True
        f.write('\n')
    # numpy.savetxt(outdir + '/' + os.path.splitext(os.path.basename(filename))[0] + ".csv", a, delimiter=",")
    

def generateMFCCData():
    global DIR
    global OUTDIR

    for f in glob.glob(OUTDIR + '/*.csv'):
        os.remove(f)

    for f in glob.glob(DIR + '/*.wav'):
        try:
            writeMFCC(f, OUTDIR)
            # newfilename = os.path.splitext(os.path.basename(f))[0]
            # print('YES: '+ newfilename)
            # os.rename(f, DIR+"/classify-me/" + newfilename+".wav")
            # os.rename(DIR+'/' + newfilename + ".mp3", DIR+"/classify-me/" + newfilename+".mp3")
        except:
            print('NO: '+f)


if __name__ == '__main__':
    writeGenresToDisk()
    generateMFCCData()

