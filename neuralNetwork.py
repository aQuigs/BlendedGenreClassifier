#!/usr/bin/python

from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer

from glob import glob
import sys, os, glob, string, csv
wd = os.path.dirname(os.path.realpath(__file__))
DIR = wd + '/songdata'

# from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
# from scipy import diag, arange, meshgrid, where
# from numpy.random import multivariate_normal

GENRE_DICT = {
    'Punk Rock'   : 0,
    'Rap Rock'    : 1,
    'Pop'         : 2,
    'Alternative' : 3,
    'Hard Rock'   : 4,
    'Rap'         : 5
}
NUMBER_OF_GENRES = 6
INPUT_DIMS = 40

alldata = ClassificationDataSet(INPUT_DIMS, 1, nb_classes=NUMBER_OF_GENRES)
for filename in glob.glob(DIR + '/*.csv'):
    basename = os.path.splitext(filename)[0]
    data = None
    genre = None
    with open(filename, 'rb') as fhandle:
        data = list(csv.reader(fhandle))[0]
        data = map(float, data)
    with open(basename + '.genre', 'r') as fhandle:
        genre = fhandle.readline()
    alldata.addSample(data, [GENRE_DICT[genre]])

tstdata_temp, trndata_temp = alldata.splitWithProportion(0.2)

tstdata = ClassificationDataSet(INPUT_DIMS, 1, nb_classes=NUMBER_OF_GENRES)
for n in xrange(0, tstdata_temp.getLength()):
    tstdata.addSample(tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1])

trndata = ClassificationDataSet(INPUT_DIMS, 1, nb_classes=NUMBER_OF_GENRES)
for n in xrange(0, trndata_temp.getLength()):
    trndata.addSample(trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1])

trndata._convertToOneOfMany()
tstdata._convertToOneOfMany()

fnn = buildNetwork(trndata.indim, 15, trndata.outdim, outclass=SoftmaxLayer)

trainer = BackpropTrainer(fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

for i in range(20):
    trainer.trainEpochs(5)
    trnresult = percentError(trainer.testOnClassData(),
                              trndata['class'])
    tstresult = percentError(trainer.testOnClassData(
           dataset=tstdata), tstdata['class'])
    print "epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult
