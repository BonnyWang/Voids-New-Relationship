import string;
import numpy as np;
import matplotlib.pyplot as plt;


fileIn = "./untrimmed_centers_central_CMASS.out";
lines = [];

R_max = 0;
R_min = 0;

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
    plotRelationship(lines, 4,8);

   
    print(findMaxValue(lines, 4));
