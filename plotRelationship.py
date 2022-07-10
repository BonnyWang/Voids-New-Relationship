from numpy import linspace
import pandas as pd;
import matplotlib.pyplot as plt;



ellipAllFile = "Merged_Radius_Ellip_All.txt";
densityAllFile = "Merged_Radius_Density_Contrast";
bins = linspace(9,63,19);
csfont = {'fontname':'Times New Roman'};
# Head: radius(Mpc/h) ellip
# Head: radius densitycontrast

def getMeanSTD(fileName, statName, binName, bins):
    df = pd.read_csv(fileName, sep=" ");
    
    df["bin"] = pd.cut(df[binName], bins=bins);
    
    binnedData = pd.DataFrame();
    binnedData["mean"] = df.groupby("bin")[statName].mean();
    binnedData["std"] = df.groupby("bin")[statName].std();
    binnedData["binMean"] = [(bins[i] + bins[i+1])/2 for i in range(len(bins) - 1)];
    
    binnedData["binMean"].reset_index(drop=True);
    return binnedData;

def plotRelationship(dataFrame, xAxis, yAxis, outputName):
    plt.errorbar(x = dataFrame["binMean"], y = dataFrame["mean"], yerr = dataFrame["std"], fmt='o', markersize = 3, capsize = 3, elinewidth = 1);
    plt.xlabel(xAxis, **csfont, fontsize = 14);
    plt.ylabel(yAxis, **csfont, fontsize = 14);
    plt.savefig(outputName + ".pdf");
    plt.show();

if __name__ == "__main__":
    
    # ellipData = getMeanSTD(ellipAllFile,"ellip","radius(Mpc/h)",bins);
    # plotRelationship(ellipData, "Radius(Mpc/h)", "Ellipticity", "radiusEllipPlot");
   
    densityData = getMeanSTD(densityAllFile,"densitycontrast", "radius",bins);
    plotRelationship(densityData, "Radius(Mpc/h)", "Density contrast", "radiusDCPlot");
    
    
    