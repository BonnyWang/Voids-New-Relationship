import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# df = pd.read_csv("Merged_DC_Ellip", sep = " ")

# ellip = np.array(df["Ellip"])
# DC = np.array(df["DC"])

# plt.scatter(ellip, DC, s=0.02)
# plt.xlim(-0.5,1.5)
# plt.ylim(0,15)
# plt.xlabel("Ellipticity")
# plt.ylabel("Density Contrast")
# plt.show()

# df1 = pd.read_csv("Merged_Radius_Ellip_All.txt", sep = " ")
# radius = np.array(df1["radius(Mpc/h)"])
# el = np.array(df1["ellip"])

# plt.scatter( el, radius, s=0.02)
# plt.ylim(0,230)
# plt.xlim(-0.5,1.5)
# plt.xlabel("Ellipticity")
# plt.ylabel("Radius")
# plt.show()


df2 = pd.read_csv("./newData/void_Quijote_HR_1406_ss1.0_z0.00_d00.out", sep = " ")
# radii = np.array(df2["radius"])
dc = np.array(df2["densitycontrast"])

dfDC_More_35 = df2.loc[df2["densitycontrast"] > 10]
# dfbinned = pd.qcut(dfDC_More_35["densitycontrast"], q = 4)
print(dfDC_More_35)
