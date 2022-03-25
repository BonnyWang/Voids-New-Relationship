import pandas as pd;

fd = "P:\Globus\mfiducial_663_halos.dat"
data = pd.read_csv(fd, sep=" ");
print(data["x"][:100]);