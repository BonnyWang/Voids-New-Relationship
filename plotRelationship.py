from operator import index
from os import sep
import string
import numpy as np;
import matplotlib.pyplot as plt;
import pandas as pd
from sqlalchemy import false;


fileIn = "./untrimmed_centers_central_CMASS.out";
lines = [];

R_max = 0;
R_min = 0;

bin_Number = 10;
binColumn = 4;
# 8 is the density contrast and 
statisticsColumn = 8;



def fileProcess():
    fd = open(fileIn);
    
    lines = fd.readlines();
    
    lines = lines[1:];
    
    return lines;

def findMaxValue(lines, Column):
    max = 0; 
    for line in lines:
        datas = line.split(" ");
        if float(datas[Column]) > max:
            max = float(datas[Column]);

    return max;

def divdeIntoBins(bin_Number, max, min = 0):
    bins= np.zeros(bin_Number);

    bin_Size = (max - min)/bin_Number;

    for index in range(bin_Number):
        bins[index] = bin_Size*(index+1);
    
    return bins;

def calculateBinStatistics(lines, bins, binColumn, statisticColumn):

    statisticsEachBin = np.zeros(bins.size);
    statisticsNumber = np.zeros(bins.size);

    for line in lines:
        datas = np.array(line.split(" ")).astype(np.float);
        for index in range(bins.size):
            if (datas[binColumn] < bins[index]) and (datas[binColumn] > (bins[index-1] if index-1 >= 0 else 0)):
                # Data belone to curent bin 
                statisticsEachBin[index] += datas[statisticColumn];
                statisticsNumber[index] += 1;
    
    
    # Normalize
    for index in range(statisticsEachBin.size):
        statisticsEachBin[index] = statisticsEachBin[index]/statisticsNumber[index]
    
    return statisticsEachBin;
            


def plotRelationship(lines,column1,column2):
    x = [];
    y = [];

    for line in lines:
        datas = line.split(" ");
        x.append(datas[column1]);
        y.append(datas[column2]);
    
    x = np.array(x);
    y = np.array(y);

    plt.scatter(x, y);
    plt.show();
    
def mergeTwoByColumn(file1, file2, key ,outFile):
    data1 = pd.read_csv(file1, sep=" ");
    data2 = pd.read_csv(file2, sep=" ");
    
    output = pd.merge(data1, data2, on=key, how="inner");
    
    output[["voidID","radius(Mpc/h)", "ellip"]].to_csv(outFile,sep=" ", index=False);
    
if __name__ == "__main__":
    
    
    lines = fileProcess();
    
    R_max = findMaxValue(lines, binColumn);
    bins = divdeIntoBins(bin_Number,R_max);
    
    fileContainRadius = "./sample_Quijote_663_ss1.0_z0.00_d00/sky_positions_all_Quijote_663_ss1.0_z0.00_d00.out";
    fileContainEllip = "./sample_Quijote_663_ss1.0_z0.00_d00/shapes_all_Quijote_663_ss1.0_z0.00_d00.out";
    mergeTwoByColumn(fileContainRadius, fileContainEllip,"voidID","./Merged.txt")
    
    # This is for whithin the file
    # statisticBins = calculateBinStatistics(lines,bins,binColumn,statisticsColumn);
    
    # print(bins);
    # print(statisticBins);
    
    # print(findMaxValue(lines, statisticsColumn))
    
    # plt.scatter(bins, statisticBins);
    # plt.show();

    # plotRelationship(lines, 4,8);

   
    # print(findMaxValue(lines, 4));
