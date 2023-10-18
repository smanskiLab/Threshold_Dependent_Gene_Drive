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

def plot(df,summarized,c0,cErr):

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

    plt.show()



#Core Loop

df = pd.read_csv('stats_cOnly.csv')

for x in range(len(df['File'])):

    dPoints = pd.read_csv(df['File'][x])

    dPoints,summarized = assemble(dPoints)
    
    xData = summarized['init_ratio_egi']
    yData = summarized['avg']

    plot(dPoints,summarized,df['C'][x],df['cErr'][x])
