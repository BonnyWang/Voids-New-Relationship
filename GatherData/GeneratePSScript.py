preCommand = "globus transfer 6b4101f6-8b6e-11ec-8fde-dfc5b31adbac:/latin_hypercube/z0.0/";
pathToChange = "Quijote_0_ss1.0/sample_Quijote_0_ss1.0_z0.00_d00/sky_positions_all_Quijote_0_ss1.0_z0.00_d00.out"

outputFile = open("transferFromGlobus.ps1", "w");

for i in range(2000):
    
    i = str(i);
    psCommandForRadius = "globus transfer 6b4101f6-8b6e-11ec-8fde-dfc5b31adbac:/latin_hypercube/z0.0/Quijote_HR_" + i + "_ss1.0/sample_Quijote_HR_" + i + "_ss1.0_z0.00_d00/centers_all_Quijote_HR_" + i + "_ss1.0_z0.00_d00.out e3a96de0-975d-11ec-bf89-ab28bf5d96bb:/~/P/Globus/sample_Quijote_HR_"+ i +"_ss1.0_z0.00_d00/centers_all_Quijote_HR_" + i + "_ss1.0_z0.00_d00.out\n";
    
    outputFile.write(psCommandForRadius);
    
    psCommandEllips = "globus transfer 6b4101f6-8b6e-11ec-8fde-dfc5b31adbac:/latin_hypercube/z0.0/Quijote_HR_" + i + "_ss1.0/sample_Quijote_HR_" + i + "_ss1.0_z0.00_d00/shapes_all_Quijote_HR_" + i + "_ss1.0_z0.00_d00.out e3a96de0-975d-11ec-bf89-ab28bf5d96bb:/~/P/Globus/sample_Quijote_HR_"+ i +"_ss1.0_z0.00_d00/shapes_all_Quijote_" + i + "_ss1.0_z0.00_d00.out\n";
    
    outputFile.write(psCommandEllips);