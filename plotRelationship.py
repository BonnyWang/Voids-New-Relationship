from asyncio.windows_events import INFINITE
from importlib.metadata import files
import numpy as np;
import matplotlib.pyplot as plt;
import pandas as pd
from pytest import skip

filesContainRadius = [];
filesContainEllips = [];

def checkFileMissing():
    for i in range(2000):
        try:
            open(filesContainRadius[i]);
        except FileNotFoundError:
            print(i);

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
    # output[["radius(Mpc/h)", "ellip"]].to_csv(outFile,sep=" ",mode="a", index=False, header=False);
    output[["radius(Mpc/h)", "ellip"]].to_csv(outFile,sep=" ", index=False);

def divideToBins(file, binColumnName, binNumber,statColumnName, outFile):
    try:
        open(file, "r");
    except FileNotFoundError:
        return;
    
    
    data = pd.read_csv(file, sep=" ");
    
    # data[binColumnName] = data[binColumnName];
    # data[statColumnName] = data[statColumnName];
    
    # min_value = data[statColumnName].min();
    # max_value = data[statColumnName].max();
    
    bins = np.linspace(0,1,binNumber+1);
    
    # Change the last number so that all the voids are included
    bins[0] = 0;
    bins[len(bins)-1] = INFINITE;
    
    # print(bins)
    
    data["bin"] = pd.cut(data[statColumnName], bins=bins);
    

    # print(data["bin"].value_counts());
    
    # Print the percentage of voids fall into the categorization compare to the whole dataset 
    print(data["bin"].value_counts().sum()/ data.shape[0]);
    
    binnedData = data.groupby("bin").count()/data.shape[0];
    
    
    # Use the middle value for each bin instead of bin average
    # binnedData[binColumnName] = [(bins[i] + bins[i+1])/2 for i in range(len(bins) - 1)];
    # Set the bin value as the middle range but include the ones that are bigger
    # binnedData[binColumnName] = [i for i in np.linspace(10.5,61.5,18)];
    
    binnedData_std = data.groupby("bin").std()
    
    
    # binnedData[[binColumnName, statColumnName]].to_csv(outFile ,sep=" ");
    
    # Fill in all the blanks with 0;
    binnedData.fillna(0, inplace=True);
    
    # Rename for quick result
    # TODO: need to change later
    # binnedData = binnedData.rename(columns={binColumnName: 'R', statColumnName: 'VSF'})
    
    binnedData[statColumnName].loc[::-1].reset_index(drop=True).to_csv(outFile);
    
    return binnedData, binnedData_std;

# also for initial processing
def createAllEllipRadiusFile():
    for i in range(2000):
        ChangeFirstLine(filesContainRadius[i]);
        ChangeFirstLine(filesContainEllips[i]);
        mergeTwoByColumn(filesContainRadius[i], filesContainEllips[i],"voidID",Merged_Radius_Ellip);

def generateRelation_per_Simulation():     
    for i in range(2000):
        outputFilePath = "./Data/sample_Quijote_HR_"+str(i) + "_ss1.0_z0.00_d00/relationship_Radius_Ellip_"+ str(i) + ".out";
        mergeTwoByColumn(filesContainRadius[i], filesContainEllips[i],"voidID", outputFilePath);

def generateAbundance_Ellip():
    for i in range(2000):
        inputFilePath = "./Data/sample_Quijote_HR_"+str(i) + "_ss1.0_z0.00_d00/relationship_Radius_Ellip_"+ str(i) + ".out";
        outFilePath = "./Abundance/abundance_z=0.0_" + str(i) + "_HR_linspace_60_5_19bins_untrimmed.csv";
        
        divideToBins(inputFilePath,"radius(Mpc/h)",18,"ellip",outFilePath);
        

def generateAbundance_DensityContrast():
    for i in range(2000):
        inputFilePath = "./Data/sample_Quijote_HR_"+str(i) + "_ss1.0_z0.00_d00/centers_all_Quijote_HR_"+ str(i) + "_ss1.0_z0.00_d00.out";
        outFilePath = "./Abundance/abundance_z=0.0_" + str(i) + "_HR_linspace_60_5_19bins_untrimmed.csv";
        
        divideToBins(inputFilePath,"radius(Mpc/h)",18,"densitycontrast",outFilePath);  
 
if __name__ == "__main__":
    
    
    Merged_Radius_Ellip = "./Merged_Radius_Density_Contrast";
    
    generateAllPath();
    
    # checkFileMissing();
    
    # generateAbundance_Ellip();
    # generateAbundance_DensityContrast();
    
    data = pd.read_csv(Merged_Radius_Ellip, sep=" ");
    bins = np.linspace(data["densitycontrast"].min(),4,19);
    data["bin"] = pd.cut(data["densitycontrast"], bins=bins);
    print(data.groupby("bin").count().loc[::-1]);
    print(data["densitycontrast"].min());
    print(data["densitycontrast"].max());
        

    
    # To plot the relationship
    # bin_Radius_Ellip, bin_Radius_Ellip_std = divideToBins(Merged_Radius_Ellip,"radius(Mpc/h)",18,"ellip","ellipBined.txt");
    
    # bin_Radius_Ellip.plot.scatter(x="radius(Mpc/h)", y="ellip", yerr=bin_Radius_Ellip_std);
    # plt.savefig("10.5_61.5_Ellip_Radius.pdf")
    # plt.show();

    # #print(bin_Radius_Ellip.head())
    
    
    # FileContainDensity = "./untrimmed_centers_central_CMASS.out";
    
    # bin_Radius_CenterDensity, bin_Radius_CenterDensity_std = divideToBins(FileContainDensity,"radius(Mpc/h)",18,"densityContrast","densityContrastBined.txt");
    # bin_Radius_CenterDensity.plot.scatter(x="radius(Mpc/h)", y="densityContrast", yerr=bin_Radius_CenterDensity_std);
    # plt.show();
