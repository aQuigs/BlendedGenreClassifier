#!/usr/bin/python

from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer, LinearLayer, SigmoidLayer
from pybrain.structure import FeedForwardNetwork, FullConnection
from amplitudeChange import analyzeFile
from pydub import AudioSegment
from mfcc import getData
from random import shuffle
import numpy

from glob import glob
import sys, os, glob, string, csv
wd = os.path.dirname(os.path.realpath(__file__))
DIR = wd + '/songdata/subset'
SONG_FILE_DIR = '/home/quiggles/Desktop/513music/single-genre/classify-me/subset'

GENRE_DICT = {
    'Punk Rock'    : 0,
    'Rap Rock'     : 1,
    'Pop'          : 2,
    'Alternative'  : 3,
    'Hard Rock'    : 4,
    'Rap'          : 5,
    'Country'      : 6,
    'Classical'    : 7,
    'R&B'          : 8,
    'Techno'       : 9,
    'Classic Rock' : 10,
    'Indie'        : 11,
    'Instrumental' : 12,
    'Folk'         : 13
}
NUMBER_OF_GENRES = len(GENRE_DICT)
INPUT_DIMS = (26)*4

def classifySegments():
    global NUMBER_OF_GENRES
    global INPUT_DIMS
    global GENRE_DICT
    global DIR

    SEGMENT_LENGTH = 1000
    PROCESSING_FILENAME = DIR + '/processing.wav'
    # AMP_PROCESSING_FILENAME = DIR + '/processing.amp'
    TRAINING_DATA_PROPORTION = 0.8
    TRAINING_EPOCHS = 80

    print('Reading training data...')
    trndata_temp = ClassificationDataSet(INPUT_DIMS, 1, nb_classes=NUMBER_OF_GENRES)
    g = glob.glob(DIR + '/*.csv')
    shuffle(g)
    for filename in g[:int(TRAINING_DATA_PROPORTION*len(g))]:
        basename = os.path.splitext(filename)[0]
        data = None
        genre = None
        with open(filename, 'rb') as fhandle:
            data = list(csv.reader(fhandle))[0]
            data = map(float, data)
        with open(basename + '.genre', 'r') as fhandle:
            genre = fhandle.readline()
        trndata_temp.addSample(data, [GENRE_DICT[genre]])
    print('Reading data done')
    # tstdata_temp, trndata_temp = alldata.splitWithProportion(0.2)

    # tstdata = ClassificationDataSet(INPUT_DIMS, 1, nb_classes=NUMBER_OF_GENRES)
    # for n in xrange(0, tstdata_temp.getLength()):
        # tstdata.addSample(tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1])

    trndata = ClassificationDataSet(INPUT_DIMS, 1, nb_classes=NUMBER_OF_GENRES)
    for n in xrange(0, trndata_temp.getLength()):
        trndata.addSample(trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1])

    trndata._convertToOneOfMany()
    # tstdata._convertToOneOfMany()
    ## Manual build
    # fnn = FeedForwardNetwork()
    # outlayer = SoftmaxLayer(trndata.outdim)
    # inlayer = LinearLayer(INPUT_DIMS)
    # hiddenLayer = SigmoidLayer(60)
    # fnn.addInputModule(inlayer)
    # fnn.addModule(hiddenLayer)
    # fnn.addOutputModule(outlayer)
    # fnn.addConnection(FullConnection(inlayer, hiddenLayer))
    # fnn.addConnection(FullConnection(hiddenLayer, outlayer))
    # fnn.sortModules()

    fnn = buildNetwork(trndata.indim, 60, trndata.outdim, outclass=SoftmaxLayer)

    mistakenDict = dict()
    for x in GENRE_DICT.keys():

        # temp = dict()
        # for y in GENRE_DICT.keys():
        #     temp[y] = 0
        # mistakenDict[x] = temp
        mistakenDict[x] = [0] * NUMBER_OF_GENRES

    print('Training...')
    trainer = BackpropTrainer(fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)
    trainer.trainEpochs(TRAINING_EPOCHS)
    print('Training done')

    print('Classifying test data segments...')
    # totalAccuracy = 0.0
    # songCount = 0
    # totalCorrectlyClassified = 0
    genreSongCount = [0] * NUMBER_OF_GENRES
    correctlyClassifiedSongCount = [0] * NUMBER_OF_GENRES
    averageSegmentAccuracies=[0] * NUMBER_OF_GENRES
    for filename in g[int(TRAINING_DATA_PROPORTION*len(g)):]:
        basename = os.path.splitext(os.path.basename(filename))[0]
        print('Processing ' + basename + '...')
        song = AudioSegment.from_wav(SONG_FILE_DIR + '/' + basename + '.wav')
        segment = song
        i = 0
        genreCounts = [0] * NUMBER_OF_GENRES
        try:
            while segment.duration_seconds:
                segment = song[i:i+SEGMENT_LENGTH]
                i += SEGMENT_LENGTH
                segment.export(PROCESSING_FILENAME, format='wav')
                inputs = getData(PROCESSING_FILENAME).tolist()
                # otherStuff = analyzeFile(PROCESSING_FILENAME)
                # inputs.append(otherStuff[0])
                # inputs.append(otherStuff[1])
                # inputs.append(otherStuff[2])
                # inputs.append(otherStuff[3])
                genreConfidences = list(fnn.activate(inputs))
                segmentGenreIndex = genreConfidences.index(max(genreConfidences))
                genreCounts[segmentGenreIndex] += 1
                os.remove(PROCESSING_FILENAME)
        except:
            print('Except at: ' + str(genreCounts))
            os.remove(PROCESSING_FILENAME)
        
        thisSongGenre = genreCounts.index(max(genreCounts))
        trueGenre = None
        with open(DIR + '/' + basename + '.genre', 'r') as f:
            trueGenre = f.readline()
        genreIndex = GENRE_DICT[trueGenre]
        accuracy = genreCounts[genreIndex] / float(sum(genreCounts))
        genreSongCount[genreIndex] += 1
        averageSegmentAccuracies[genreIndex] += accuracy
        if thisSongGenre == genreIndex:
            correctlyClassifiedSongCount[genreIndex] += 1

        print("%5.2f%% accurate for '%s'" % (100*accuracy, basename))

        mistakenList = mistakenDict[trueGenre]
        total = float(sum(genreCounts))
        for j in xrange(len(genreCounts)):
            mistakenList[j] += genreCounts[j] / total

        # totalAccuracy += accuracy
        # songCount += 1
    print('Done classifying segments')
    for k in mistakenDict:
        for v in xrange(len(mistakenDict[k])):
            if genreSongCount[v] > 0:
                mistakenDict[k][v] /= float(genreSongCount[v])
                mistakenDict[k][v] *= 100

    for k in GENRE_DICT:
        i = GENRE_DICT[k]
        print('-'*75)
        print('Total songs classified in %s genre: %d' % (k, genreSongCount[i]))
        if genreSongCount[i]:
            print('Total song classification accuracy for %s: %5.2f%%' % (k, 100.0*correctlyClassifiedSongCount[i]/genreSongCount[i]))
            print('Average segment classification accuracy for %s: %5.2f%%' % (k, 100.0*averageSegmentAccuracies[i]/genreSongCount[i]))
            print('Mistakes: ' + str(mistakenDict[k]))
    totalSongCount = sum(genreSongCount)
    totalAccuracy = sum(averageSegmentAccuracies)
    correctlyClassifiedSongs = sum(correctlyClassifiedSongCount)
    print('='*75)
    print('Total songs tested: %d' % totalSongCount)
    print('Average segment classification accuracy per song: %5.2f%%' % (100.0*totalAccuracy/totalSongCount))
    print('Total accuracy for properly identified songs: %5.2f%%' % (100.0*correctlyClassifiedSongs/totalSongCount))

## Deprecated
# def classifyWhole():
#     global NUMBER_OF_GENRES
#     global INPUT_DIMS
#     global GENRE_DICT
#     global DIR

#     alldata = ClassificationDataSet(INPUT_DIMS, 1, nb_classes=NUMBER_OF_GENRES)
#     for filename in glob.glob('DIR' + '/*.csv'):
#         basename = os.path.splitext(filename)[0]
#         data = None
#         genre = None
#         with open(filename, 'rb') as fhandle:
#             data = list(csv.reader(fhandle))[0]
#             data = map(float, data)
#         with open(basename + '.genre', 'r') as fhandle:
#             genre = fhandle.readline()
#         alldata.addSample(data, [GENRE_DICT[genre]])

#     tstdata_temp, trndata_temp = alldata.splitWithProportion(0.2)

#     tstdata = ClassificationDataSet(INPUT_DIMS, 1, nb_classes=NUMBER_OF_GENRES)
#     for n in xrange(0, tstdata_temp.getLength()):
#         tstdata.addSample(tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1])

#     trndata = ClassificationDataSet(INPUT_DIMS, 1, nb_classes=NUMBER_OF_GENRES)
#     for n in xrange(0, trndata_temp.getLength()):
#         trndata.addSample(trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1])

#     trndata._convertToOneOfMany()
#     tstdata._convertToOneOfMany()

#     fnn = buildNetwork(trndata.indim, 15, trndata.outdim, outclass=SoftmaxLayer)

#     trainer = BackpropTrainer(fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

#     for i in range(20):
#         trainer.trainEpochs(5)
#         trnresult = percentError(trainer.testOnClassData(),
#                                   trndata['class'])
#         tstresult = percentError(trainer.testOnClassData(
#                dataset=tstdata), tstdata['class'])
#         print "epoch: %4d" % trainer.totalepochs, \
#               "  train error: %5.2f%%" % trnresult, \
#               "  test error: %5.2f%%" % tstresult

if __name__ == '__main__':
    classifySegments()
