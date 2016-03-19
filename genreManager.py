#!/usr/bin/python

import sys, os, glob, string
wd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(wd + '/pytagger-0.5')
sys.path.append(wd + '/pytagger-0.5/tagger')
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
            elif frame.strings[0] == '(14)':
                frame.set_text('R&B')
            elif frame.strings[0] == '(17)':
                frame.set_text('Rock')
            elif frame.strings[0] == '(14)R&B':
                frame.set_text('R&B')
            elif frame.strings[0] == '(1)':
                frame.set_text('Classic Rock')
            elif frame.strings[0] == '(2)':
                frame.set_text('Country')
            tag.commit()

def listGenre(filename, masterdict):
    tag = ID3v2(filename)
    for frame in tag.frames:
        if frame.fid == 'TCON':
            genre = frame.strings[0].split('\x00')[0]
            if genre in masterdict:
                masterdict[genre] += 1
            else:
                masterdict[genre] = 1

def writeGenresToDisk(indir, outdir):
    for f in glob.glob(outdir + '/*.genre'):
        os.remove(f)

    # masterdict = dict()
    for f in glob.glob(indir + '/*.mp3'):
        writeGenre(f, outdir)
        # updateGenre(f)
        # listGenre(f, masterdict)
    # print(str(masterdict))

if __name__ == '__main__':
    writeGenresToDisk('/home/quiggles/Desktop/513music/single-genre/classify-me', '/home/quiggles/BlendedGenreClassifier/songdata')
