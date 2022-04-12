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
    
    # Not working
    # chi, p = chisquare(omegaM__Predicted, omegaM_True);


if __name__ == "__main__":
    getChiValue();