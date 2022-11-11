import math
from msilib.schema import Directory
from unittest import result
import pandas as pd;
import numpy as np;
from prettytable import PrettyTable
from pylab import *

rcParams["mathtext.fontset"]='cm'

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

def calculateForEllipAll(fileName):
    data = pd.read_csv(filename, sep=" ", header=None);
    
    omegaM_True = data.iloc[:,0].to_numpy().ravel();    
    omegaM_Predicted = data.iloc[:,2].to_numpy().ravel();
    omegaM_Error = data.iloc[:,4].to_numpy().ravel();
    
    ns_True = data.iloc[:,1].to_numpy().ravel();    
    ns_Predicted = data.iloc[:,3].to_numpy().ravel();
    ns_Error = data.iloc[:,5].to_numpy().ravel();
    
    resultTable = PrettyTable(["Parameter","RMSE","RSqaure", "ErrorOver_Prediction", "chiValue"]);
    
    getMesurements(omegaM_Predicted,omegaM_True,omegaM_Error, "OmegaM",resultTable);
    getMesurements(ns_Predicted,ns_True,ns_Error, "ns",resultTable);
    
    resultTable.float_format = '.4';
    print("Ellip:");
    print(resultTable);
    
def calculateForDensityContrastl():
    data = pd.read_csv("./Borrars/borrardcwithMean2Para100trial1.txt", sep=" ", header=None);
    
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

def plotData(out_File, data_True, data_Predict, data_Std, parameterName):
    
    Directory = "./Plots/"
    
    RMSE = getRMSE(data_Predict, data_True);
    RSqaure = getRSquare_Coefficent(data_Predict, data_True);
    ErrorOver_Prediction = getErrorOver_Prediction(data_Predict, data_Std);
    chiValue = getChiValue(data_Predict, data_True, data_Std);
    
    # Only select 40 to plot
    np.random.seed(18)
    indexes = np.random.choice(np.arange(data_True.shape[0]),40,replace=False)
    data_True = data_True[indexes]
    data_Predict = data_Predict[indexes]
    data_Std = data_Std[indexes]
    
    extendValue = (data_True.max() - data_True.min())/30
    x_Range = [data_True.min() - extendValue, data_True.max() + extendValue ]
    y_Range = [data_True.min()- extendValue , data_True.max()+extendValue ]
    
    fig=figure()
    ax1=fig.add_subplot(111) 
    ax1.set_xlabel(r'${\rm True}$',fontsize=18)
    ax1.set_ylabel(r'${\rm Inference}$',fontsize=18)
    p1=ax1.errorbar(data_True, data_Predict, data_Std,lw=1,fmt='o',ms=2,
                elinewidth=1,capsize=5,linestyle='None') 
    p1=ax1.plot(x_Range, y_Range,linestyle='-',marker='None',c='k')
    # print(x_Range, y_Range)
    props = dict(boxstyle='square', facecolor='white', alpha=0.07)
    ax1.text(0.05,0.9, parameterName, fontsize=18, color='k',transform=ax1.transAxes)
    ax1.text(0.7,0.07,rf"$\chi^2 = {chiValue:.2f}$" +"\n"+ rf"$R^2 = {RSqaure:.2f}$" + "\n"+ r"${\rm RMSE} = $"+ f"{RMSE:.2f}$"  + "\n" + r"${\rm MMRE} = $"+ f"{ErrorOver_Prediction:.2f}$", fontsize=15, color='k',transform=ax1.transAxes,  bbox=props)
    savefig(Directory + out_File, bbox_inches='tight')
    show()
    close(fig)

def plotAll(fileName):
    file = fileName
    data = np.loadtxt(file)
    
    gap = 5
    i_Omega = 0
    i_Sigma = 4
    plotData("./Deepset_OmegaM.pdf",data[:,i_Omega], data[:,i_Omega + gap], data[:,i_Omega + gap*2], r"$\Omega_{\rm m}$")
    plotData("./Deepset_Sigma8.pdf",data[:,i_Sigma], data[:,i_Sigma + gap], data[:,i_Sigma + gap*2], r"$\sigma_{\rm 8}$")
    plotData("./Deepset_Ns.pdf",data[:,3], data[:,8], data[:,13], r"$n_{\rm s}$")

def calculateEpstemic(groupName, index):
    # Get the initial Size
    allValues = np.loadtxt(groupName +  "0.txt")
    allValues = allValues[np.newaxis, :]
    
    for i in range(1,10):
        data = np.loadtxt(f"{groupName}{i}.txt")
        data = data[np.newaxis, :]
        allValues = np.append(allValues,  data, axis=0)
    
    # print(allValues[:,:,index])
    error = np.std(allValues[:,:,index], axis=0)
    
    print(np.mean(error))

def calcAleatoric(fileName, index):
    file = fileName
    data = np.loadtxt(file)
    
    print(np.mean(data[:,index]))
        

if __name__ == "__main__":
   
    # for i in range(10):
    #     filename = f"./Borrars/borrardcwithMean2Para100trial{i}.txt"    
    #     # print("Ellip:");    
    #     # calculateForEllipAll(filename);
    #     plotAll(filename)
    
    # print("Density Contrast:");
    # calculateForDensityContrastl();
    
    # file = "./Borrars/borrardcwithMean2Para100trial"
    # calculateEpstemic(file,2)
    # calcAleatoric(file + "0.txt", 4)
    
    plotAll("./Results_edr.txt")
    # plotAll('./Results_edr.txt')