from numpy import linspace
import pandas as pd;
import matplotlib.pyplot as plt;
import seaborn as sns

rc = {"font.family" : "serif", 
      "mathtext.fontset" : "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

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
    plt.xlabel(r"$R$ (Mpc/h)", **csfont, fontsize = 14);
    plt.ylabel(r"$\rho$", **csfont, fontsize = 14, fontstyle='italic');
    # plt.ylim(0, 0.35);
    plt.savefig(outputName + ".pdf");
    plt.show();
    
    


if __name__ == "__main__":
    
    # ellipData = getMeanSTD(ellipAllFile,"ellip","radius(Mpc/h)",bins);
    # plotRelationship(ellipData, "Radius(Mpc/h)", "Ellipticity", "radiusEllipPlot");
    
    # df = pd.read_csv(ellipAllFile, sep=" ");
    # bins = linspace(10.5, 61.5, 18)
    # d = df["radius(Mpc/h)"].to_numpy().flatten()
    # sns.histplot(d,bins=bins,stat="density", color="skyblue")
    # plt.xlabel("Radius(Mpc/h)", **csfont, fontsize = 14);
    # plt.ylabel("Density", **csfont, fontsize = 14);
    # # plt
    # plt.show()
   
    densityData = getMeanSTD(densityAllFile,"densitycontrast", "radius",bins);
    plotRelationship(densityData, "Radius(Mpc/h)", "Density contrast", "radiusDCPlot");
    
    
    # df = pd.read_csv(densityAllFile, sep=" ")
    # dcRange = df.loc[(df["densitycontrast"] > 1.0) & (df["densitycontrast"] < 3.5)]
    # print(len(dcRange));
    # range = dcRange.shape[0]/df.shape[0]
    
    # print(range);
    
    