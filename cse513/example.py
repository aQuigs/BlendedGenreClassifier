from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav
import fileinput
import numpy

def example(filename, filenamefullpath, directoryforprocessedcsv):

    print(filenamefullpath)
    (rate,sig) = wav.read(filenamefullpath)
    mfcc_feat = mfcc(sig,rate)
    fbank_feat = logfbank(sig,rate)
    a = numpy.asarray(mfcc_feat)
    numpy.savetxt(directoryforprocessedcsv + filename + ".csv", a, delimiter=",")
    #file = open('C:\\Users\\Mel\\Desktop\\cse513\\musicstuff\\' + filename + '.txt', "w")
    #file.write(str(mfcc_feat.toList()).replace('],[', ';', end=''))
    #file.close()
    print(numpy.average(a));

#print(str(mfcc_feat[:,:])