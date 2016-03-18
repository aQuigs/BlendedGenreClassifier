#!/usr/bin/python

import sys, os, glob, string
wd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(wd + '/pytagger-0.5')
sys.path.append(wd + '/pytagger-0.5/tagger')
sys.path.append(wd + '/python_speech_features')
from tagger import ID3v2

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

def listGenre(filename, masterset):
    tag = ID3v2(filename)
    for frame in tag.frames:
        if frame.fid == 'TCON':
            masterset.add(frame.strings[0].split('\x00')[0])

if __name__ == '__main__':
    DIR = '/home/quiggles/Desktop/513music/single-genre'
    OUTDIR = wd + '/songdata'
    for f in glob.glob(OUTDIR + '/*.genre'):
        os.remove(f)


    # masterset = set()
    for f in glob.glob(DIR + '/*.mp3'):
        writeGenre(f, OUTDIR)
        # updateGenre(f)
        # listGenre(f, masterset)
    # print(str(masterset))
 
