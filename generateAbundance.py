from asyncio.windows_events import INFINITE
from cgi import print_arguments
from importlib.metadata import files
import os
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
    
    
def mergeTwoByColumn(file1, file2, key ,outFile, i):
    
    try:
        open(file1, "r");
    except FileNotFoundError:
        return;
        
    
    data1 = pd.read_csv(file1, sep=" ");
    data2 = pd.read_csv(file2, sep=" ");
    
    output = pd.merge(data1, data2, on=key, how="inner");
    
    if not data1.loc[data1["densitycontrast"] > 10].empty:
        print(i);
        
    
    # output[["voidID","radius(Mpc/h)", "ellip"]].to_csv(outFile,sep=" ", index=False);
    
    # Removed voidID since there are repeated ID in different simulation
    # Use concatination to the output instead of create a new file. 
    # output[["radius(Mpc/h)", "ellip"]].to_csv(outFile,sep=" ",mode="a", index=False, header=False);
    # output.rename(columns = {",centerx":"x", "z(Mpc/h)":"z"}, inplace = True)
    # output[["index","x"]] = output["x"].str.split(",", expand=True)
    # output[["voidID", "ellip", "densitycontrast"]].to_csv(outFile,sep=" ", index=False, mode="a", header=False);

def divideToBins(file, binNumber,statColumnName, outFile):
    try:
        open(file, "r");
    except FileNotFoundError:
        return;
    
    
    data = pd.read_csv(file, sep=" ");
    
    # min_value = data[statColumnName].min();
    # max_value = data[statColumnName].max();
    
    # bins = np.linspace(0.99,4.5,binNumber+1);
    bins = np.linspace(0.99,3,binNumber+1);
    
    # Change the last number so that all the voids are included
    bins[0] = 0;
    bins[len(bins)-1] = INFINITE;
        
    data["bin"] = pd.cut(data[statColumnName], bins=bins);
    

    # print(data["bin"].value_counts());
    # Print the percentage of voids fall into the categorization compare to the whole dataset 
    # print(data["bin"].value_counts().sum()/ data.shape[0]);
    
    binnedData = data.groupby("bin").count()/data.shape[0];
    # print(data.groupby("bin")[statColumnName].mean());
    binnedData["mean"] = data.groupby("bin")[statColumnName].mean();
    
    
    # binnedData_std = data.groupby("bin").std()
        
    # Fill in all the blanks with 0;
    binnedData.fillna(0, inplace=True);
    
    binnedData[[statColumnName, "mean"]].reset_index(drop=True).to_csv(outFile);
    
    return binnedData;

# also for initial processing
def createAllEllipRadiusFile():
    for i in range(2000):
        # ChangeFirstLine(filesContainRadius[i]);
        # ChangeFirstLine(filesContainEllips[i]);
        mergeTwoByColumn(filesContainRadius[i], filesContainEllips[i],"voidID","Merged_DC_Ellip", i);

def generateRelation_per_Simulation():     
    for i in range(2000):
        outputFilePath = "./newData/void_Quijote_HR_"+ str(i) + "_ss1.0_z0.00_d00.out";
        mergeTwoByColumn(filesContainRadius[i], filesContainEllips[i],"voidID", outputFilePath);

def generateAbundance_Ellip():
    for i in range(2000):
        inputFilePath = "./Data/sample_Quijote_HR_"+str(i) + "_ss1.0_z0.00_d00/relationship_Radius_Ellip_"+ str(i) + ".out";
        outFilePath = "./Abundance/abundance_z=0.0_" + str(i) + "_HR_linspace_60_5_19bins_untrimmed.csv";
        
        divideToBins(inputFilePath,18,"ellip",outFilePath);
        # getMeanStd(inputFilePath,"radius(Mpc/h)",18,"ellip",outFilePath);
        

def generateAbundance_DensityContrast():
    nVoid = 0
    nfile = 0
    for i in range(2000):
        inputFilePath = "./Data/sample_Quijote_HR_"+str(i) + "_ss1.0_z0.00_d00/centers_all_Quijote_HR_"+ str(i) + "_ss1.0_z0.00_d00.out";
        outFilePath = "./Abundance/abundance_z=0.0_" + str(i) + "_HR_linspace_60_5_19bins_untrimmed.csv";
        
        try:
            open(inputFilePath, "r");
        except FileNotFoundError:
            continue
    
    
        data = pd.read_csv(inputFilePath, sep=" ");
        
        nVoid += data.shape[0]
        nfile += 1
    print(nVoid)
    print(nfile)
        
        # divideToBins(inputFilePath,18,"densitycontrast",outFilePath);  
        
    # divideToBins(inputPath,"radius(Mpc/h)",18,"radius(Mpc/h)","radius?"); 
    
def combine_DensityandEllip():
    for i in range(2000):
        combineFilePath = "./Abundance/abundance_z=0.0_" + str(i) + "_HR_linspace_60_5_19bins_untrimmed.csv";
        densityContrastPath = "./Abundance/abundance_z=0.0_" + str(i) + "_HR_linspace_60_5_19bins_untrimmed.csv.d";
        if not(os.path.exists(combineFilePath)): continue;
        
        cDF = pd.read_csv(combineFilePath);
        dcDF = pd.read_csv(densityContrastPath);

        cDF["densitycontrast"] = dcDF["densitycontrast"];
        
        cDF[['densitycontrast', 'ellip']].to_csv(combineFilePath);
        os.remove(densityContrastPath);                              
                              

 
if __name__ == "__main__":
    
    
    # Merged_Radius_Ellip = "./Merged_Radius_Density_Contrast";
    
    generateAllPath();
    # generateRelation_per_Simulation();
    # createAllEllipRadiusFile()
    
    # checkFileMissing();
    
    # generateAbundance_Ellip();
    generateAbundance_DensityContrast();
    
    # combine_DensityandEllip();
    
    # exploreRadius();
    
    # data = pd.read_csv(Merged_Radius_Ellip, sep=" ");
    # bins = np.linspace(0.99,4.5,19);
    # data["bin"] = pd.cut(data["densitycontrast"], bins=bins);
    # print(data.groupby("bin").count().loc[::-1]);
    # print(data["bin"].value_counts().sum()/ data.shape[0]);
    # print(data["densitycontrast"].min());
    # print(data["densitycontrast"].max());
        

    
    # To plot the relationship
    # bin_Radius_Ellip, bin_Radius_Ellip_std = divideToBins(Merged_Radius_Ellip,"radius(Mpc/h)",18,"ellip","ellipBined.txt");
    
    # bin_Radius_Ellip.plot.scatter(x="radius(Mpc/h)", y="ellip", yerr=bin_Radius_Ellip_std);
    # plt.savefig("10.5_61.5_Ellip_Radius.pdf")
    # plt.show();

    # #print(bin_Radius_Ellip.head())
    
    
    # FileContainDensity = "./untrimmed_centers_central_CMASS.out";
    
    # bin_Radius_CenterDensity, bin_Radius_CenterDensity_std = divideToBins(FileContainDensity,"radius(Mpc/h)",18,"densityContrast","densityContrastBined.txt");
    # bin_Radius_CenterDensity.plot.scatter(x="radius(Mpc/h)", y="densityContrast", yerr=bin_Radius_CenterDensity_std);
    # plt.savefig("density_contrast_Radius.pdf")
    # plt.show();
