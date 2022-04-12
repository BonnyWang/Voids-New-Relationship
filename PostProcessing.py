import math
from operator import length_hint
from scipy.stats import chisquare
import pandas as pd;
import numpy as np;

# Chi value test

def getChiValue(observed, expected):
    chiValue = 0;
    
    for i in range(len(expected)):
        differance = observed[i] - expected[i];
        squared = math.pow(differance,2);
        chiValue += squared/expected[i];
    
    print("chiValue is "+str(chiValue));
    
    # Not working
    # print(chisquare(observed,expected))
    
    return chiValue;


if __name__ == "__main__":
        
    data = pd.read_csv("./Data/borrarEllipAll.txt", sep=" ", header=None);
    
    omegaM_True = data.iloc[:,0].to_numpy().ravel();    
    omegaM_Predicted = data.iloc[:,5].to_numpy().ravel();
    
    ns_True = data.iloc[:,3].to_numpy().ravel();    
    ns_Predicted = data.iloc[:,8].to_numpy().ravel();
    
    getChiValue(omegaM_Predicted, omegaM_True);
    getChiValue(ns_Predicted, ns_True);