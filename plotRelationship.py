import string;
import numpy as np;
import matplotlib.pyplot as plt;


fileIn = "./untrimmed_centers_central_CMASS.out";
lines = [];

R_max = 0;
R_min = 0;

bin_Number = 10;


def fileProcess():
    fd = open(fileIn);
    lines = fd.readlines();
    lines = lines[50:1000];
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

if __name__ == "__main__":
    lines = fileProcess();

    R_max = findMaxValue(lines, 4);
    print(divdeIntoBins(bin_Number,R_max))

    # plotRelationship(lines, 4,8);

   
    # print(findMaxValue(lines, 4));
