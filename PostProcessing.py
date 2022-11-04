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

def calculateForEllipAll():
    data = pd.read_csv("./Borrars/borrarDCMean36Para2.txt", sep=" ", header=None);
    
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
    data = pd.read_csv("./Borrars/Results_all_Paco.txt", sep=" ", header=None);
    
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
    y_Range = [data_Predict.min()- extendValue , data_Predict.max()+extendValue ]
    
    fig=figure()
    ax1=fig.add_subplot(111) 
    ax1.set_xlabel(r'${\rm True}$',fontsize=18)
    ax1.set_ylabel(r'${\rm Inference}$',fontsize=18)
    p1=ax1.errorbar(data_True, data_Predict, data_Std,lw=1,fmt='o',ms=2,
                elinewidth=1,capsize=5,linestyle='None') 
    p1,=ax1.plot(x_Range, y_Range,linestyle='-',marker='None',c='k')
    props = dict(boxstyle='square', facecolor='grey', alpha=0.07)
    ax1.text(0.05,0.9, parameterName, fontsize=18, color='k',transform=ax1.transAxes)
    ax1.text(0.74,0.07,rf"$\chi^2 = {chiValue:.2f}$" +"\n"+ rf"$R^2 = {RSqaure:.2f}$" + "\n"+ rf"$RMSE = {RMSE:.2f}$"  + "\n" + rf"$MMRE = {ErrorOver_Prediction:.2f}$", fontsize=12, color='k',transform=ax1.transAxes,  bbox=props)
    savefig(Directory + out_File, bbox_inches='tight')
    show()
    close(fig)

def plotAll(fileName):
    file = fileName
    data = np.loadtxt(file)
    
    
    plotData("./Deepset_OmegaM.png",data[:,0], data[:,5], data[:,10], r"$\Omega_{\rm m}$")
    plotData("./Deepset_Sigma8.png",data[:,4], data[:,9], data[:,14], r"$\sigma_{\rm 8}$")
    plotData("./Deepset_Ns.png",data[:,3], data[:,8], data[:,13], r"$n_{\rm s}$")



if __name__ == "__main__":
    
    # print("Ellip:");    
    # calculateForEllipAll();
    
    # print("Density Contrast:");
    # calculateForDensityContrastl();
    
    plotAll('./Results_edr.txt')