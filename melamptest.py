from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import fft, arange, ifft
from numpy import sin, linspace, pi
from scipy.io.wavfile import read,write
import csv
from itertools import izip



def AnalyzeFile(filename):
    rate,data=read(filename)
    y=data[:,1]
    lungime=len(y)
    timp=len(y)/44100
    t=linspace(0,timp,len(y))
    subplot(2,1,1)
    plot(t,y)
    xlabel('Time')
    ylabel('Amplitude')
    #WriteToCSV(filename,t,y)
    Sort(filename,t,y)
    


def WriteToCSV(filename, t,y):
    with open(filename + '.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(izip(t, abs(y)))
    
def Sort(filename, t,y):
    
    under1000 = 0
    under2000 = 0
    under3000 = 0
    under4000 = 0
    under5000 = 0
    under6000 = 0
    under7000 = 0
    under8000 = 0
    under9000 = 0
    under10000 = 0
    anythingelse = 0
    
    for blah in y:
        if blah < 1000:
            under1000 = under1000 + 1
        elif blah < 2000:
            under2000 = under2000 + 1
        elif blah < 3000:
            under3000 = under3000 + 1
        elif blah < 4000:
            under4000 = under4000 + 1
        elif blah < 5000:
            under5000 = under5000+1
        elif blah < 6000:
            under6000 = under6000+1
        elif blah < 7000:
            under7000 = under7000+1
        elif blah < 8000:
            under8000 = under8000+1
        elif blah < 9000:
            under9000 = under9000+1
        elif blah < 10000:
            under10000 = under10000+1
        else:
            anythingelse = anythingelse + 1
    
    print(under1000/float(len(y)))
    print(under2000/float(len(y)))
    print(under3000/float(len(y)))
    print(under4000/float(len(y)))
    print(under5000/float(len(y)))
    print(under6000/float(len(y)))
    print(under7000/float(len(y)))
    print(under8000/float(len(y)))
    print(under9000/float(len(y)))
    print(under10000/float(len(y)))
    print(anythingelse/float(len(y)))    

    #NEED TO FIGURE OUT HOW TO PUT THE VALUES OF THE PERCENTAGES INTO A NICE PLACE
        
        
AnalyzeFile('hellopeople.wav')   




