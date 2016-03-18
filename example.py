from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav
import fileinput
import numpy

def example(filename, filenamefullpath, directoryforprocessedcsv):

    print(filenamefullpath)
    (rate,sig) = wav.read(filenamefullpath)
    mfcc_feat = mfcc(sig,rate)
    #fbank_feat = logfbank(sig,rate)
    #a = numpy.asarray(mfcc_feat)
    l = len(mfcc_feat)/4
    quartileMean1 = numpy.mean(mfcc_feat[:l],      axis=0)
    quartileMean2 = numpy.mean(mfcc_feat[l:2*l],   axis=0)
    quartileMean3 = numpy.mean(mfcc_feat[2*l:3*l], axis=0)
    quartileMean4 = numpy.mean(mfcc_feat[3*l:],    axis=0)

    a = numpy.concatenate([quartileMean1, quartileMean2, quartileMean3, quartileMean4])
    numpy.savetxt(directoryforprocessedcsv + filename + ".csv", a, delimiter=",")


    #file = open('C:\\Users\\Mel\\Desktop\\cse513\\musicstuff\\' + filename + '.txt', "w")
    #file.write(str(mfcc_feat.toList()).replace('],[', ';', end=''))
    #file.close()
    print(numpy.average(a));

#print(str(mfcc_feat[:,:])