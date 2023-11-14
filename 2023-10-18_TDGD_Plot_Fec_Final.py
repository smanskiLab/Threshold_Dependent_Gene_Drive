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

def plot(df,summarized,c0,cErr,F0,Ferr,title,Thr,SEM):

    fig, ax1 = plt.subplots(figsize=(10,6))

    #generate function space
    Xarr=np.linspace(0,1,100)

    CX=np.multiply(c0,Xarr) 

    C2=np.multiply(np.subtract(1,CX),np.subtract(1,CX))

    dim=np.add(np.multiply(F0,np.multiply(CX,CX)),C2)

    Yarr=np.subtract(np.divide(np.multiply(F0,np.multiply(CX,CX)),dim),Xarr)
    #/generate function space

    R = Rsquared(df,summarized,c0,F0)
    plt.scatter(df['init_ratio_egi'],df['delta'])

    plt.plot(Xarr,Yarr)

    plt.ylim(-0.5,0.5)

    plt.plot(Xarr,np.zeros(len(Xarr)),color = 'r')
    plt.axvline(Thr)
    plt.axvline(Thr+SEM)
    plt.axvline(Thr-SEM)

    plt.title(title+' R2 = '+str(R))

    plt.savefig('Fec'+title+'.svg')
    plt.savefig('Fec'+title+'.png')

def Rsquared(df,summarized,C,F):

    #delMean
    delMean = 0
    delFunc = 0
    for x in range(len(df['init_ratio_egi'])):

        temp = summarized[summarized['init_ratio_egi']==df['init_ratio_egi'][x]]

        temp = temp.reset_index()

        delMean += (df['delta'][x]-temp['avg'][0])**2

        delFunc += (df['delta'][x]-funky(df['init_ratio_egi'][x],C,F))**2

    R = 1 - delFunc/delMean
        
    return(R)

def funky(Xarr,c0,F0):

    CX=np.multiply(c0,Xarr) 

    C2=np.multiply(np.subtract(1,CX),np.subtract(1,CX))

    dim=np.add(np.multiply(F0,np.multiply(CX,CX)),C2)

    Yarr=np.subtract(np.divide(np.multiply(F0,np.multiply(CX,CX)),dim),Xarr)

    return(Yarr)

#Core Loop

df = pd.read_csv('stats.csv')

for x in range(len(df['File'])):

    dPoints = pd.read_csv(df['File'][x])

    dPoints,summarized = assemble(dPoints)
    
    xData = summarized['init_ratio_egi']
    yData = summarized['avg']

    plot(dPoints,summarized,df['C'][x],df['cErr'][x],df['F'][x],df['fErr'][x],df['Line'][x]+'_'+str(df['Temp'][x])+'deg',df['Thr'][x],df['SEM'][x])
