#!/usr/bin/python

import sys, os, glob, string
wd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(wd + '/pytagger-0.5')
sys.path.append(wd + '/pytagger-0.5/tagger')
from tagger import ID3v2
from neuralNetwork import GENRE_DICT, NUMBER_OF_GENRES
from random import shuffle
from shutil import copyfile

def getGenre(filename):
    tag = ID3v2(filename)
    for frame in tag.frames:
        if frame.fid == 'TCON':
            return frame.strings[0].split('\x00')[0] # remove padding \x00

def writeGenre(filename, outdir):
    with open(outdir + '/' + os.path.basename(os.path.splitext(filename)[0]) + '.genre','w') as f:
        f.write(getGenre(filename))

def updateGenre(filename):
    i=0
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
            elif frame.strings[0] == 'Indie Rock':
                frame.set_text('Indie')
            elif frame.strings[0] == '(18)':
                frame.set_text('Techno')
            elif frame.strings[0] == 'Punk':
                frame.set_text('Punk Rock')
            elif frame.strings[0] == '(33)':
                frame.set_text('Instrumental')
            elif frame.strings[0] == '(80)':
                frame.set_text('Folk')
            elif frame.strings[0] == '(80)Folk':
                frame.set_text('Folk')
            elif frame.strings[0] == 'garage, lo-fi':
                frame.set_text('Alternative')
            elif frame.strings[0] == '(121)Punk Rock':
                frame.set_text('Punk Rock')
            elif frame.strings[0] == 'Hard Rock & Metal':
                frame.set_text('Hard Rock')
            elif frame.strings[0] == 'Classsic Rock':
                frame.set_text('Classic Rock')
            elif frame.strings[0] == 'Rock':
                frame.set_text('Classic Rock')
            elif frame.strings[0] == '(40)':
                frame.set_text('Alternative')
            else:
                return
            tag.commit()


def listGenre(filename, masterdict):
    genre = getGenre(filename)
    if genre in masterdict:
        masterdict[genre] += 1
    else:
        masterdict[genre] = 1

def copySubset(dir, filename):
    copyfile(dir + '/' + filename, dir + '/subset/' + filename)

def get_subset(songdir, datadir, COUNT, IGNORE_GENRES_LIST):
    # out = songdir + '/subset'
    # if os.path.exists(out):
    #     for f in glob.glob(out + '/*'):
    #         os.remove(f)
    # else:
    #     os.mkdir(out)

    # out = datadir + '/subset'
    # if os.path.exists(out):
    #     for f in glob.glob(out + '/*'):
    #         os.remove(f)
    # else:
    #     os.mkdir(out)

    genreCounts = [0]*NUMBER_OF_GENRES
    g = glob.glob(songdir + '/*.mp3')
    shuffle(g)
    for mp3File in g:
        genre = getGenre(mp3File)
        if genre not in IGNORE_GENRES_LIST and genreCounts[GENRE_DICT[genre]] < COUNT:
            genreCounts[GENRE_DICT[genre]] += 1
            basename = os.path.basename(os.path.splitext(mp3File)[0])
            copySubset(songdir, basename + '.mp3')
            copySubset(songdir, basename + '.wav')
            copySubset(datadir, basename + '.csv')
            copySubset(datadir, basename + '.genre')
            try:
                copySubset(datadir, basename + '.amp')
            except:
                pass
            if sum(genreCounts) >= NUMBER_OF_GENRES*COUNT - len(IGNORE_GENRES_LIST)*COUNT:
                break

def appendData(indir, datadir):
    g = glob.glob(datadir + '/subset/*.csv')
    for f in g:
        ampfile = os.path.splitext(f)[0] + '.logf'

        with open(f, 'rb+') as filehandle:
            filehandle.seek(-1, os.SEEK_END)
            filehandle.truncate()

        with open(f,'a') as csvHandle:
            with open(ampfile, 'r') as ampHandle:
                csvHandle.seek(-1, os.SEEK_END)
                csvHandle.write(',')
                csvHandle.write(ampHandle.readline())

# def temp(indir, datadir):
    # g = glob.glob(datadir + '/*.csv')
    # for f in g:
    #     ampfile = datadir + '/subset/' + os.path.basename(os.path.splitext(f)[0]) + '.amp'
    #     mp3file = indir + '/' + os.path.basename(os.path.splitext(f)[0]) + '.mp3'
    #     wavfile = indir + '/' + os.path.basename(os.path.splitext(f)[0]) + '.wav'
    #     if not os.path.exists(ampfile) and getGenre(mp3file) == 'Hard Rock':
    #         print(f)



        # if not os.path.exists(ampfile):
        #     if os.path.exists('/home/quiggles/BlendedGenreClassifier/songdata/' + os.path.basename(ampfile)):
        #         print(ampfile)
        #         copyfile('/home/quiggles/BlendedGenreClassifier/songdata/' + os.path.basename(ampfile), ampfile)




def temp(songdir, datadir):
    songs = set()
    for s in glob.glob(songdir + '/subset/*.mp3'):
        coreName = os.path.splitext(os.path.basename(s))[0]
        copyfile(datadir + '/' + coreName + '.genre', datadir + '/subset/' + coreName + '.genre')
        copyfile(datadir + '/' + coreName + '.csv', datadir + '/subset/' + coreName + '.csv')
        songs.add(coreName)

    # for s in glob.glob(songdir + '/subset/*.wav'):
    #     coreName = os.path.splitext(os.path.basename(s))[0]
    #     if coreName not in songs:
    #         os.remove(s)
    # for s in glob.glob(datadir + '/subset/*.csv'):
    #     coreName = os.path.splitext(os.path.basename(s))[0]
    #     if coreName not in songs:
    #         os.remove(s)

    # for s in glob.glob(datadir + '/subset/*.genre'):
    #     coreName = os.path.splitext(os.path.basename(s))[0]
    #     if coreName not in songs:
    #         os.remove(s)
    # for s in glob.glob(datadir + '/subset/*.amp'):
    #     coreName = os.path.splitext(os.path.basename(s))[0]
    #     if coreName not in songs:
    #         os.remove(s)

def removeFromSubset(songdir, datadir, genres):
    g = glob.glob(songdir + '/subset/*.mp3')
    for f in g:
        if getGenre(f) in genres:
            os.rename(f, songdir + '/badsubset/' + os.path.basename(f))
            os.rename(songdir + '/subset/' + os.path.splitext(os.path.basename(f))[0] + '.wav', songdir + '/badsubset/' + os.path.splitext(os.path.basename(f))[0] + '.wav')
            os.rename(datadir + '/subset/' + os.path.splitext(os.path.basename(f))[0] + '.csv', datadir + '/badsubset/' + os.path.splitext(os.path.basename(f))[0] + '.csv')
            os.rename(datadir + '/subset/' + os.path.splitext(os.path.basename(f))[0] + '.genre', datadir + '/badsubset/' + os.path.splitext(os.path.basename(f))[0] + '.genre')
            try:
                os.rename(f, datadir + '/badsubset/' + os.path.splitext(os.path.basename(f))[0] + '.amp')
            except:
                pass


def writeGenresToDisk(indir, outdir):
    # for f in glob.glob(outdir + '/*.genre'):
        # os.remove(f)

    # masterdict = dict()
    for f in glob.glob(indir + '/*.mp3'):
        writeGenre(f, outdir)
        # updateGenre(f)
        # listGenre(f, masterdict)
    # print(str(masterdict))

if __name__ == '__main__':
    # pass
    # removeFromSubset('/home/quiggles/Desktop/513music/single-genre/classify-me', '/home/quiggles/BlendedGenreClassifier/songdata',['Alternative'])
    # get_subset('/home/quiggles/Desktop/513music/single-genre/classify-me', '/home/quiggles/BlendedGenreClassifier/songdata', 150, ['Punk Rock', 'Rap Rock', 'Pop', 'Alternative','Hard Rock', 'Rap', 'Country', 'Classical','R&B', 'Techno','Classic Rock', 'Indie', 'Instrumental'])
    writeGenresToDisk('/home/quiggles/Desktop/513music/single-genre/classify-me/subset', '/home/quiggles/BlendedGenreClassifier/songdata')
    # temp('/home/quiggles/Desktop/513music/single-genre/classify-me', '/home/quiggles/BlendedGenreClassifier/songdata')
    # appendData('/home/quiggles/Desktop/513music/single-genre/classify-me', '/home/quiggles/BlendedGenreClassifier/songdata')
