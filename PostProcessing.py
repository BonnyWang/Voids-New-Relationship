import math
from operator import length_hint
from scipy.stats import chisquare
import pandas as pd;
import numpy as np;

# Chi value test

def getChiValue():
    
    data = pd.read_csv("./Data/borrarEllipAll.txt", sep=" ", header=None);
    
    omegaM_True = data.iloc[:,0].to_numpy().ravel();    
    omegaM__Predicted = data.iloc[:,5].to_numpy().ravel();
    
    # print(len(omegaM_True));    
    # print(len(omegaM__Predicted));    
    
    chiValue = 0;
    
    for i in range(len(omegaM_True)):
        differance = omegaM__Predicted[i] - omegaM_True[i];
        squared = math.pow(differance,2);
        chiValue += squared/omegaM_True[i];
    
    print("chiValue is "+str(chiValue));
    
    return chiValue;


if __name__ == "__main__":
    getChiValue();