import math
from operator import length_hint
from scipy.stats import chisquare
import pandas as pd;
import numpy as np;

# Chi value test

def getChiValue(observed, expected, error):
    sum = 0;
    size = len(observed)
    
    for i in range(len(expected)):
        differance = observed[i] - expected[i];
        squared = math.pow(differance,2);
        error_Divided = squared/math.pow(error[i],2);
        sum += error_Divided;
    
    chiValue = sum/size;
    
    # Not working
    # print(chisquare(observed,expected))
    
    return chiValue;


if __name__ == "__main__":
        
    data = pd.read_csv("./Data/borrarEllipAll.txt", sep=" ", header=None);
    
    omegaM_True = data.iloc[:,0].to_numpy().ravel();    
    omegaM_Predicted = data.iloc[:,5].to_numpy().ravel();
    omegaM_Error = data.iloc[:,10].to_numpy().ravel();
    
    ns_True = data.iloc[:,3].to_numpy().ravel();    
    ns_Predicted = data.iloc[:,8].to_numpy().ravel();
    ns_error = data.iloc[:,13].to_numpy().ravel();
    
    chi_OmegaM = getChiValue(omegaM_Predicted, omegaM_True,omegaM_Error);
    chi_Ns = getChiValue(ns_Predicted, ns_True, ns_error);
    
    print("OmegaM Chi Value:" + str(chi_OmegaM));
    print("Ns Chi Value:" + str(chi_Ns));