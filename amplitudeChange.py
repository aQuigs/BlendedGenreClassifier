#!/usr/bin/python

from numpy import linspace
from scipy.io.wavfile import read
from glob import glob
import os, glob
wd = os.path.dirname(os.path.realpath(__file__))


def analyzeFile(filename, outfile=None):
    if outfile is None or not os.path.exists(outfile):
        rate,data=read(filename)
        y=data[:,1]
        timp=len(y)/44100
        t=linspace(0,timp,len(y))
        localmaxpeak = 0
        localminpeak = 10000
       
        timeinsecond = 0
        timestepsize = .1
        overalllocalmaxpeak = 0
        overalllocalminpeak = 0
        overalllocalrange = 0
        # overalldistanceupanddown = 0
        overallsteps = 0
        overallchangeinrange = 0
        lastrange = 0
        lastvalue = 0
        for indexvalue, (time,value) in enumerate (zip(t,abs(y))):
            if (indexvalue == 0):
                lastvalue = value
            elif (time <= timeinsecond+timestepsize):
                # overalldistanceupanddown+=abs(value-lastvalue)
                if value > lastvalue:
                    if value < localminpeak:
                        localminpeak = value
                    if value > localmaxpeak:
                        localmaxpeak = value
            else:
                #print(timeinsecond, localmaxpeak, localminpeak, localmaxpeak-localminpeak)
                overallsteps+=1
                overalllocalmaxpeak+=localmaxpeak
                overalllocalminpeak+=localminpeak
                overalllocalrange+=abs(localmaxpeak-localminpeak)
                overallchangeinrange+=abs(lastrange - abs(localmaxpeak-localminpeak))
                
                
                lastrange = abs(localmaxpeak-localminpeak)
            

                timeinsecond = timeinsecond+timestepsize
                localmaxpeak = 0
                localminpeak = 100000000
            
            lastvalue = value;
        
        value1 = (overalllocalmaxpeak/overallsteps)
        value2 = (overalllocalminpeak/overallsteps)
        value3 = (overalllocalrange/overallsteps)
        value4 = (overallchangeinrange/overallsteps)
        # value5 = (abs(overalldistanceupanddown/timeinsecond))

        return (value1, value2, value3, value4)
    

def writeOutputs(outputs, outfile):
    with open(outfile, 'w') as f:
        # f.write(',')
        f.write(str(outputs[0]))
        f.write(',')
        f.write(str(outputs[1]))
        f.write(',')
        f.write(str(outputs[2]))
        f.write(',')
        f.write(str(outputs[3]))
        # f.write(',')
        # f.write(str(value5))

def generateOutputs(indir, outdir):
    # for f in glob.glob(outdir + '/*.amp'):
        # os.remove(f)

    for f in glob.glob(indir + '/*.wav'):
        # print('Processing ' + os.path.basename(f) + '...')
        try:
            writeOutputs(analyzeFile(f), outdir + '/' + os.path.splitext(os.path.basename(f))[0] + ".amp")
        except:
            print("ERROR: " + f)



if __name__ == '__main__':
    generateOutputs('/home/quiggles/Desktop/513music/single-genre/classify-me/subset', '/home/quiggles/BlendedGenreClassifier/songdata/subset')
