import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import numpy, scipy, matplotlib
import matplotlib.pyplot as plt
import warnings
import sys


def assemble(df):

    df['delta']=df['EGI']/(df['OREO']+df['EGI'])-df['init_ratio_egi']

    summarized = df.groupby('init_ratio_egi',as_index=False).agg(
        avg = pd.NamedAgg(column="delta", aggfunc="min"),
        stdev = pd.NamedAgg(column="delta", aggfunc="std"))

    return(df,summarized)

def plot(df,summarized,c0,cErr,title,Thr,SEM):

    fig, ax1 = plt.subplots(figsize=(10,6))

    #generate function space
    Xarr=np.linspace(0,1,100)

    CX=np.multiply(c0,Xarr) 

    C2=np.multiply(np.subtract(1,CX),np.subtract(1,CX))

    dim=np.add(np.multiply(1,np.multiply(CX,CX)),C2)

    Yarr=np.subtract(np.divide(np.multiply(1,np.multiply(CX,CX)),dim),Xarr)
    #/generate function space

    #generate Upper function space
    Xarr=np.linspace(0,1,100)

    CX=np.multiply(c0+cErr,Xarr) 

    C2=np.multiply(np.subtract(1,CX),np.subtract(1,CX))

    dim=np.add(np.multiply(1,np.multiply(CX,CX)),C2)

    YUp=np.subtract(np.divide(np.multiply(1,np.multiply(CX,CX)),dim),Xarr)
    #/generate Upper function space

    R = Rsquared(df,summarized,c0)

    #generate Lower function space
    Xarr=np.linspace(0,1,100)

    CX=np.multiply(c0-cErr,Xarr) 

    C2=np.multiply(np.subtract(1,CX),np.subtract(1,CX))

    dim=np.add(np.multiply(1,np.multiply(CX,CX)),C2)

    YLow=np.subtract(np.divide(np.multiply(1,np.multiply(CX,CX)),dim),Xarr)
    #/generate Lower function space

    plt.scatter(df['init_ratio_egi'],df['delta'])

    plt.plot(Xarr,Yarr)

    plt.fill_between(Xarr,YUp,YLow,alpha = 0.1, color = 'b')

    plt.ylim(-0.5,0.5)

    plt.plot(Xarr,np.zeros(len(Xarr)),color = 'r')
    plt.axvline(Thr)
    plt.axvline(Thr+SEM)
    plt.axvline(Thr-SEM)

    plt.gca().set_aspect('equal')

    plt.title(title+' R2 = '+str(R))

    plt.savefig('0_'+title+'.svg')
    plt.savefig('0_'+title+'.png')

def Rsquared(df,summarized,C):

    #delMean
    delMean = 0
    delFunc = 0
    for x in range(len(df['init_ratio_egi'])):

        temp = df['delta'].mean()

        delMean += (df['delta'][x]-temp)**2

        delFunc += (df['delta'][x]-funky(df['init_ratio_egi'][x],C))**2

    R = 1 - delFunc/delMean
    print(delFunc,delMean, R)
    input()
        
    return(R)

def funky(Xarr,c0):

    CX=np.multiply(c0,Xarr) 

    C2=np.multiply(np.subtract(1,CX),np.subtract(1,CX))

    dim=np.add(np.multiply(1,np.multiply(CX,CX)),C2)

    Yarr=np.subtract(np.divide(np.multiply(1,np.multiply(CX,CX)),dim),Xarr)

    return(Yarr)

#Core Loop

df = pd.read_csv('stats_cOnly.csv')

for x in range(len(df['File'])):

    dPoints = pd.read_csv(df['File'][x])

    dPoints,summarized = assemble(dPoints)
    
    xData = summarized['init_ratio_egi']
    yData = summarized['avg']

    plot(dPoints,summarized,df['C'][x],df['cErr'][x],df['Line'][x]+'_'+str(df['Temp'][x])+'deg',df['Thr'][x],df['SEM'][x])
