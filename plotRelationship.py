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
    lines = lines[1:];
    return lines;

def findMaxValue(lines, Column):
    max = 0; 
    for line in lines:
        datas = line.split(" ");
        if float(datas[Column]) > max:
            max = float(datas[Column]);

    return max;


if __name__ == "__main__":
    lines = fileProcess();
    N = 50;
    x = np.random.rand(N);
    y = np.random.rand(N);

    plt.scatter(x, y);
    plt.show();
    print(findMaxValue(lines, 4));
