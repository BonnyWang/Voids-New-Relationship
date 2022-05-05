import math
from unittest import result
import pandas as pd;
import numpy as np;
from prettytable import PrettyTable

def getMesurements(predicted, expected, error, parameter_Name, resultTable):
    RMSE = getRMSE(predicted, expected);
    RSqaure = getRSquare_Coefficent(predicted, expected);
    ErrorOver_Prediction = getErrorOver_Prediction(predicted, error);
    chiValue = getChiValue(predicted, expected, error);
    
    print(parameter_Name + "'s RMSE is " + str(RMSE));
    print(parameter_Name + "'s Rsqaured is " + str(RSqaure));
    print(parameter_Name + "'s |Error|/Prediction is " + str(ErrorOver_Prediction));
    print(parameter_Name + "'s chiValue is " + str(chiValue));
    
    print("");
    
    resultTable.add_row([parameter_Name, RMSE, RSqaure, ErrorOver_Prediction, chiValue]);
    
    return RMSE, RSqaure, ErrorOver_Prediction, chiValue;
    
# Normalized chi value
def getChiValue(predicted, expected, error):
    sum = 0;
    size = len(predicted)
    
    for i in range(len(expected)):
        differance = predicted[i] - expected[i];
        squared = math.pow(differance,2);
        error_Divided = squared/math.pow(error[i],2);
        sum += error_Divided;
    
    chiValue = sum/size;
    
    
    return chiValue;

def getRMSE(predicted, expected):
    MSE = np.square(np.subtract(expected,predicted)).mean(); 
 
    RMSE = math.sqrt(MSE);
    
    return RMSE;

def getRSquare_Coefficent(predicted, expected):
    RSS =np.square(np.subtract(expected, predicted)).sum();
    TSS = np.square(np.subtract(expected, np.mean(expected))).sum();
    
    RSquared = 1 - RSS/TSS;
    
    return RSquared;
    
def getErrorOver_Prediction(predicted, error):
    return np.divide(np.abs(error), predicted).mean();

def calculateForEllipAll():
    data = pd.read_csv("./Data/borrarEllipAll.txt", sep=" ", header=None);
    
    omegaM_True = data.iloc[:,0].to_numpy().ravel();    
    omegaM_Predicted = data.iloc[:,5].to_numpy().ravel();
    omegaM_Error = data.iloc[:,10].to_numpy().ravel();
    
    ns_True = data.iloc[:,3].to_numpy().ravel();    
    ns_Predicted = data.iloc[:,8].to_numpy().ravel();
    ns_Error = data.iloc[:,13].to_numpy().ravel();
    
    resultTable = PrettyTable(["Parameter","RMSE","RSqaure", "ErrorOver_Prediction", "chiValue"]);
    
    getMesurements(omegaM_Predicted,omegaM_True,omegaM_Error, "OmegaM",resultTable);
    getMesurements(ns_Predicted,ns_True,ns_Error, "ns",resultTable);
    
    resultTable.float_format = '.4';
    print("Ellip:");
    print(resultTable);
    
def calculateForDensityContrastl():
    data = pd.read_csv("./borrarDensityContrast1.txt", sep=" ", header=None);
    
    omegaM_True = data.iloc[:,0].to_numpy().ravel();    
    omegaM_Predicted = data.iloc[:,5].to_numpy().ravel();
    omegaM_Error = data.iloc[:,10].to_numpy().ravel();
    
    ns_True = data.iloc[:,3].to_numpy().ravel();    
    ns_Predicted = data.iloc[:,8].to_numpy().ravel();
    ns_Error = data.iloc[:,13].to_numpy().ravel();
    
    sigma8_True = data.iloc[:,4].to_numpy().ravel();    
    sigma8_Predicted = data.iloc[:,9].to_numpy().ravel();
    sigma8_Error = data.iloc[:,14].to_numpy().ravel();
    
    resultTable = PrettyTable(["Parameter","RMSE","RSqaure", "ErrorOver_Prediction", "chiValue"]);
    
    getMesurements(omegaM_Predicted,omegaM_True, omegaM_Error, "omegaM", resultTable);
    getMesurements(ns_Predicted,ns_True, ns_Error, "ns", resultTable);
    getMesurements(sigma8_Predicted,sigma8_True, sigma8_Error, "sigma8", resultTable);
    
    resultTable.float_format = '.4';
    print("Density Contrast:");
    print(resultTable);

if __name__ == "__main__":
    
    print("Ellip:");    
    calculateForEllipAll();
    
    print("Density Contrast:");
    calculateForDensityContrastl();