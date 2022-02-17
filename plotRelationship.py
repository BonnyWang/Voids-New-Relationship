from operator import index
import numpy as np;
import matplotlib.pyplot as plt;
import pandas as pd

    
def mergeTwoByColumn(file1, file2, key ,outFile):
    data1 = pd.read_csv(file1, sep=" ");
    data2 = pd.read_csv(file2, sep=" ");
    
    output = pd.merge(data1, data2, on=key, how="inner");
    
    output[["voidID","radius(Mpc/h)", "ellip"]].to_csv(outFile,sep=" ", index=False);

def divideToBins(file, binColumnName, binNumber,statColumnName, outFile):
    data = pd.read_csv(file, sep=" ");
    data["bin"] = pd.qcut(data[binColumnName], q=binNumber);
    
    
    # print(data["bin"].value_counts());
    binnedData = data.groupby("bin").mean();
    binnedData[[binColumnName, statColumnName]].to_csv(outFile,sep=" ");
    
    return binnedData;
    
if __name__ == "__main__":
    
    
    Merged_Radius_Ellip = "./Merged_Radius_Ellip.txt";
    
    fileContainRadius = "./sample_Quijote_663_ss1.0_z0.00_d00/sky_positions_all_Quijote_663_ss1.0_z0.00_d00.out";
    fileContainEllip = "./sample_Quijote_663_ss1.0_z0.00_d00/shapes_all_Quijote_663_ss1.0_z0.00_d00.out";
    
    mergeTwoByColumn(fileContainRadius, fileContainEllip,"voidID",Merged_Radius_Ellip);
        
    bin_Radius_Ellip = divideToBins(Merged_Radius_Ellip,"radius(Mpc/h)",10,"ellip","ellipBined.txt");
    
    bin_Radius_Ellip.plot.scatter(x="radius(Mpc/h)", y="ellip");
    plt.show();
    
    
    FileContainDensity = "./untrimmed_centers_central_CMASS.out";
    
    bin_Radius_CenterDensity = divideToBins(FileContainDensity,"radius(Mpc/h)",10,"densityContrast","densityContrastBined.txt");
    bin_Radius_CenterDensity.plot.scatter(x="radius(Mpc/h)", y="densityContrast");
    plt.show();
