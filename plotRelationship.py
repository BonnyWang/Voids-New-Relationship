from importlib.metadata import files
import numpy as np;
import matplotlib.pyplot as plt;
import pandas as pd
from pytest import skip

filesContainRadius = [];
filesContainEllips = [];

def ChangeFirstLine(file):
    try:
        fp = open(file, "r");
    except FileNotFoundError:
        # print(file);
        return;
    
    lines = fp.readlines();
    
    fp = open(file, "w");
    
    # lines[0] = lines[0].replace(" ","");
    # lines[0] = lines[0].replace(","," ");
    lines[0] = lines[0].replace("#", "");
        
    fp.writelines(lines);
    fp.close();

def generateAllPath():
    for i in range(2000):
        i = str(i);
        
        fileRadius = "./Data/sample_Quijote_HR_"+ i +"_ss1.0_z0.00_d00/centers_all_Quijote_HR_" + i + "_ss1.0_z0.00_d00.out";
        
        filesContainRadius.append(fileRadius);
        
        fileEllips = "./Data/sample_Quijote_HR_"+ i +"_ss1.0_z0.00_d00/shapes_all_Quijote_HR_" + i + "_ss1.0_z0.00_d00.out";
        
        filesContainEllips.append(fileEllips);
    
    
def mergeTwoByColumn(file1, file2, key ,outFile):
    
    try:
        open(file1, "r");
    except FileNotFoundError:
        return;
        
    
    data1 = pd.read_csv(file1, sep=" ");
    data2 = pd.read_csv(file2, sep=" ");
    
    output = pd.merge(data1, data2, on=key, how="inner");
    
    # output[["voidID","radius(Mpc/h)", "ellip"]].to_csv(outFile,sep=" ", index=False);
    
    # Removed voidID since there are repeated ID in different simulation
    # Use concatination to the output instead of create a new file. 
    output[["radius(Mpc/h)", "ellip"]].to_csv(outFile,sep=" ",mode="a", index=False, header=False);

def divideToBins(file, binColumnName, binNumber,statColumnName, outFile):
    data = pd.read_csv(file, sep=" ");
    
    # data[binColumnName] = data[binColumnName];
    # data[statColumnName] = data[statColumnName];
    
    # min_value = data[binColumnName].min();
    # max_value = data[binColumnName].max();
    
    bins = np.linspace(10.5,61.5,binNumber);
    
    data["bin"] = pd.cut(data[binColumnName], bins=bins);
    

    print(data["bin"].value_counts());
    
    # Print the percentage of voids fall into the categorization compare to the whole dataset 
    print(data["bin"].value_counts().sum()/ data.shape[0]);
    
    binnedData = data.groupby("bin").mean();
    
    
    # Use the middle value for each bin instead of bin average
    binnedData[binColumnName] = [(bins[i] + bins[i+1])/2 for i in range(len(bins) - 1)];
    
    binnedData_std = data.groupby("bin").std()
    
    
    binnedData[[binColumnName, statColumnName]].to_csv(outFile ,sep=" ");
    
    return binnedData, binnedData_std;
    
if __name__ == "__main__":
    
    
    Merged_Radius_Ellip = "./Merged_Radius_Ellip_All.txt";
    
    generateAllPath();
    
    # for i in range(2000):
        # ChangeFirstLine(filesContainRadius[i]);
        # ChangeFirstLine(filesContainEllips[i]);
        # mergeTwoByColumn(filesContainRadius[i], filesContainEllips[i],"voidID",Merged_Radius_Ellip);
        
    bin_Radius_Ellip, bin_Radius_Ellip_std = divideToBins(Merged_Radius_Ellip,"radius(Mpc/h)",18,"ellip","ellipBined.txt");
    
    bin_Radius_Ellip.plot.scatter(x="radius(Mpc/h)", y="ellip", yerr=bin_Radius_Ellip_std);
    plt.show();
    # #print(bin_Radius_Ellip.head())
    
    
    # FileContainDensity = "./untrimmed_centers_central_CMASS.out";
    
    # bin_Radius_CenterDensity, bin_Radius_CenterDensity_std = divideToBins(FileContainDensity,"radius(Mpc/h)",18,"densityContrast","densityContrastBined.txt");
    # bin_Radius_CenterDensity.plot.scatter(x="radius(Mpc/h)", y="densityContrast", yerr=bin_Radius_CenterDensity_std);
    # plt.show();
